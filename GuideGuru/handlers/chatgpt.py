import openai
import os
import glob

from bs4 import BeautifulSoup
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import CallbackQuery

from config_data import config
from filters.is_author import IsAuthorFilter
from states.overall import OverallState


CHATGPT_API_KEY = config.CHATGPT_API_KEY
openai.api_key = CHATGPT_API_KEY

router_chatgpt = Router()


@router_chatgpt.message(Command("chatgpt"), IsAuthorFilter())
@router_chatgpt.callback_query(F.data == "chatgpt")
async def chatgpt(message, state):
    if isinstance(message, CallbackQuery):
        message = message.message
    await message.answer("Задавай вопрос")
    await state.set_state(OverallState.chatgpt)


@router_chatgpt.message(OverallState.chatgpt)
async def chatgpt_answer(message):
    result = query_instruction(message.text)
    await message.answer(result)


def load_html_texts(folder_path):
    texts = []
    for file_path in glob.glob(os.path.join(folder_path, "**", "*.html"), recursive=True):
        with open(file_path, "r", encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")
        for tag in soup(["script", "style", "header", "nav", "footer"]):
            tag.decompose()
        lines = [line.strip() for line in soup.get_text(separator="\n").splitlines() if line.strip()]
        texts.append("\n".join(lines))
    return texts

# 2. Разбивка на фрагменты
splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

# Укажи здесь путь к папке с распакованными HTML
html_folder = "instructions"
raw_texts = load_html_texts(html_folder)

documents = []
for text in raw_texts:
    documents.extend(splitter.create_documents([text]))


embeddings = OpenAIEmbeddings(openai_api_key=CHATGPT_API_KEY)
index = FAISS.from_documents(documents, embeddings)
index.save_local("instruction_faiss_index")

# 4. Функция RAG-запроса

def query_instruction(question: str, k: int = 3) -> str:
    db = FAISS.load_local(
        "instruction_faiss_index",
        embeddings,
        allow_dangerous_deserialization=True
    )
    docs = db.similarity_search(question, k=k)
    context = "\n\n".join(d.page_content for d in docs)
    messages = [
        {"role": "system", "content": "Ты ассистент. Отвечай строго по контексту инструкции."},
        {"role": "user", "content": f"Инструкция:\n{context}\n\nВопрос: {question}"}
    ]
    resp = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=messages,
        temperature=0.0
    )
    return resp.choices[0].message.content
