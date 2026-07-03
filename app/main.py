import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from app.config.settings import settings
from app.database.db import engine, async_session
from app.database.models import Base

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Инициализация бота и диспетчера
bot = Bot(token=settings.BOT_TOKEN)
dp = Dispatcher()


@dp.message(Command("start"))
async def start_command(message: types.Message):
    """Обработка команды /start"""
    await message.answer(
        "👋 Привет! Это бот ClassConnect.\n\n"
        "Команды:\n"
        "/start - главное меню\n"
        "/help - справка"
    )


@dp.message(Command("help"))
async def help_command(message: types.Message):
    """Обработка команды /help"""
    await message.answer(
        "ClassConnect - бот для классов и сообществ\n\n"
        "Функции:\n"
        "• Создание класса\n"
        "• Вступление в класс\n"
        "• Создание встреч\n"
        "• Голосование\n"
        "• Дни рождения"
    )


async def init_db():
    """Инициализация БД"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("✅ База данных инициализирована")


async def main():
    """Основная функция запуска бота"""
    logger.info("🚀 Запуск бота...")
    
    # Инициализация БД
    await init_db()
    
    # Запуск polling'а (получение обновлений)
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())