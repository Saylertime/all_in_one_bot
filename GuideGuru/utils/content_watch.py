import aiohttp


async def content_watch_check(text):
    try:
        url = "https://content-watch.ru/public/api/"
        data = {
            "key": "Y1LnHQ0t6b1uUjO",
            "action": "CHECK_TEXT",
            "text": text,
            "test": 0,
        }

        headers = {"Content-Type": "application/x-www-form-urlencoded"}

        async with aiohttp.ClientSession() as session:
            async with session.post(url=url, data=data, headers=headers) as response:

                response_text = await response.text()
                try:
                    result = await response.json(content_type=None)
                except Exception:
                    raise ValueError(
                        f"Failed to parse JSON. Response text:\n{response_text}"
                    )

        msg = ""

        if result["error_code"] == 0:
            msg += f"Процент уникальности: {result['percent']}\n\n"
            if len(result["matches"]) > 0:
                for i in result["matches"]:
                    normal_url = i["url"].replace("\\/", "/")
                    msg += (
                        f"{i['percent']} процентов — скопировано отсюда: {normal_url}\n"
                    )
        else:
            msg = f"ОШИБКА: {result['error']}"

        return msg
    except Exception as e:
        return f"Ошибка: {e}"
