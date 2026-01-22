"""
МИНИМАЛЬНАЯ РАБОЧАЯ ВЕРСИЯ БОТА
Просто отвечает на команды
"""
import logging
import sys
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    stream=sys.stdout
)
logger = logging.getLogger(__name__)

# ВАШ ТОКЕН - ВСТАВЬТЕ СЮДА
BOT_TOKEN = "8251108200:AAF2wTId8BpIteJkJCf0WjaSlk-jBxCfrLo"

# ========== ПРОСТЫЕ КОМАНДЫ ==========

async def start(update: Update, context: CallbackContext):
    """Команда /start"""
    await update.message.reply_text(
        "✅ Бот работает!\n"
        "Привет! Я бот для учёта услуг.\n\n"
        "Проверка связи: ОК"
    )
    logger.info(f"Пользователь {update.effective_user.id} отправил /start")

async def echo(update: Update, context: CallbackContext):
    """Повторяет сообщение"""
    text = update.message.text
    await update.message.reply_text(f"Вы сказали: {text}")
    logger.info(f"Эхо: {text}")

async def test(update: Update, context: CallbackContext):
    """Тестовая команда"""
    await update.message.reply_text("🟢 Тест пройден! Бот активен.")

# ========== ЗАПУСК ==========

def main():
    try:
        logger.info("🚀 Запуск минимального бота...")
        
        # Создаём приложение
        app = Application.builder().token(BOT_TOKEN).build()
        
        # Добавляем обработчики
        app.add_handler(CommandHandler("start", start))
        app.add_handler(CommandHandler("test", test))
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
        
        # Настраиваем polling с правильными параметрами
        logger.info("⏳ Начинаем polling...")
        
        app.run_polling(
            drop_pending_updates=True,  # Игнорируем старые сообщения
            allowed_updates=Update.ALL_TYPES,
            poll_interval=2.0,  # Интервал опроса
            timeout=30
        )
        
    except Exception as e:
        logger.error(f"❌ Ошибка: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
