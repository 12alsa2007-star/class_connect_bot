import asyncio
import logging
from aiohttp import web

from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

from app.config.settings import settings
from app.database.db import engine
from app.database.models import Base


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = Bot(token=settings.BOT_TOKEN)
dp = Dispatcher()


# -------- HANDLERS --------

@dp.message(Command("start"))
async def start_command(message: types.Message):
    await message.answer("👋 Привет! Бот работает через webhook")


@dp.message(Command("help"))
async def help_command(message: types.Message):
    await message.answer("Команды: /start /help")


# -------- DB --------

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# -------- WEBHOOK PATH --------

WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = settings.WEBHOOK_URL   # ты добавишь в env


async def on_startup(app):
    await init_db()

    await bot.set_webhook(WEBHOOK_URL + WEBHOOK_PATH)

    logger.info("Webhook установлен")


async def on_shutdown(app):
    await bot.delete_webhook()
    await bot.session.close()


# -------- APP --------

def create_app():
    app = web.Application()

    SimpleRequestHandler(
        dispatcher=dp,
        bot=bot
    ).register(app, path=WEBHOOK_PATH)

    setup_application(app, dp, bot=bot)

    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)

    return app


if __name__ == "__main__":
    app = create_app()
    web.run_app(app, host="0.0.0.0", port=8000)
    