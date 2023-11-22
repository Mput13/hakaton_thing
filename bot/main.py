import asyncio
import configparser
import logging

from aiogram import Bot
from aiogram.enums import ParseMode
from aiogram.utils.callback_answer import CallbackAnswerMiddleware

from app import dp
from bot.models import db_session
from commands.intro import intro_router

logger = logging.getLogger(__name__)


async def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    logger.info("Starting bot")

    parser = configparser.ConfigParser()
    # Парсинг файла конфигурации
    parser.read("config/bot.ini")
    db_session.global_init("db/nigas.db")
    bot = Bot(parser.get('TG_BOT', 'token'), parse_mode=ParseMode.HTML)
    dp.include_routers(
        intro_router
    )
    dp.callback_query.middleware(CallbackAnswerMiddleware())
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
