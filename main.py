import logging
import sys
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
import config

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    stream=sys.stdout
)
logger = logging.getLogger(__name__)

# Проверяем наличие токена
if not config.BOT_TOKEN or config.BOT_TOKEN == "ВАШ_ТОКЕН_БОТА":
    logger.error("❌ ТОКЕН БОТА НЕ НАЙДЕН!")
    logger.error("Добавьте BOT_TOKEN в переменные окружения на Bothost или в config.py")
    sys.exit(1)

# Команда /start
async def start(update: Update, context: CallbackContext):
    user = update.effective_user
    logger.info(f"Пользователь {user.id} запустил бота")
    
    await update.message.reply_html(
        f"🎉 <b>Бот работает!</b>\n"
        f"Привет {user.mention_html()}!\n\n"
        f"<i>Бот успешно запущен на Bothost!</i>\n\n"
        f"Скоро добавлю:\n"
        f"• Прогресс-бар 📊\n"
        f"• Inline-кнопки 🚗\n"
        f"• Учёт услуг 💰\n\n"
        f"<code>Статус: ✅ Активен</code>"
    )

# Обработка текстовых сообщений
async def handle_message(update: Update, context: CallbackContext):
    text = update.message.text
    user = update.effective_user
    logger.info(f"Сообщение от {user.id}: {text}")
    
    await update.message.reply_text(
        f"✅ Бот получил: '{text}'\n\n"
        f"ID вашего сообщения: {update.message.message_id}\n"
        f"Ваш ID: {user.id}\n\n"
        f"<i>Функции бота скоро будут добавлены</i>",
        parse_mode='HTML'
    )

# Обработка ошибок
async def error_handler(update: Update, context: CallbackContext):
    logger.error(f"Ошибка: {context.error}", exc_info=context.error)

# Главная функция для Bothost (вебхуки)
async def setup_application():
    """Настройка приложения для Bothost"""
    logger.info("Настройка приложения...")
    
    # Создаём приложение
    application = Application.builder().token(config.BOT_TOKEN).build()
    
    # Регистрируем обработчики
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Обработчик ошибок
    application.add_error_handler(error_handler)
    
    return application

# Для запуска на Bothost (вебхуки)
app = None
try:
    logger.info("Инициализация бота...")
    app = asyncio.run(setup_application())
    logger.info("✅ Бот инициализирован успешно!")
except Exception as e:
    logger.error(f"❌ Ошибка инициализации: {e}")
    sys.exit(1)

# Функция для обработки вебхуков (нужна для Bothost)
async def handle_webhook(request):
    """Обработчик вебхуков для Bothost"""
    try:
        json_data = await request.json()
        update = Update.de_json(json_data, app.bot)
        await app.process_update(update)
        return web.Response(text="OK", status=200)
    except Exception as e:
        logger.error(f"Ошибка обработки вебхука: {e}")
        return web.Response(text="Error", status=500)

# Для локального тестирования (polling)
if __name__ == '__main__':
    import asyncio
    from aiohttp import web
    
    async def main():
        # Получаем порт из переменной окружения (для Bothost)
        port = int(os.getenv('PORT', 8080))
        
        # Создаём веб-приложение
        web_app = web.Application()
        web_app.router.add_post('/webhook', handle_webhook)
        
        # Запускаем веб-сервер
        runner = web.AppRunner(web_app)
        await runner.setup()
        site = web.TCPSite(runner, '0.0.0.0', port)
        
        logger.info(f"🚀 Веб-сервер запущен на порту {port}")
        await site.start()
        
        # Бесконечный цикл
        await asyncio.Event().wait()
    
    asyncio.run(main())
