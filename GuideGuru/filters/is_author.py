from aiogram.filters import BaseFilter
from aiogram.types import CallbackQuery
from psql_maker import find_author


class IsAuthorFilter(BaseFilter):
    async def __call__(self, message):
        username = "@" + message.from_user.username
        name_in_db = await find_author(username)
        return bool(name_in_db)
