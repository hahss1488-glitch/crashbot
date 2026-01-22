"""
ПРОСТОЙ РАБОЧИЙ БОТ ДЛЯ БЕСПЛАТНОГО ТАРИФА BOTHOST
"""
import logging
import sys
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
import config

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    stream=sys.stdout
)
logger = logging.getLogger(__name__)

# Проверяем токен
if config.BOT_TOKEN.startswith("ВАШ_ТОКЕН"):
    logger.error("❌ ЗАМЕНИТЕ ТОКЕН В config.py!")
    logger.error("1. Получите токен у @BotFather")
    logger.error("2. Вставьте его в config.py в BOT_TOKEN")
    sys.exit(1)

# ========== КОМАНДЫ БОТА ==========

# /start - главная команда
async def start(update: Update, context: CallbackContext):
    user = update.effective_user
    
    # Приветственное сообщение
    await update.message.reply_html(
        f"🎉 <b>Добро пожаловать, {user.first_name}!</b>\n\n"
        f"Я бот для учёта услуг на работе.\n\n"
        f"<b>Доступные команды:</b>\n"
        f"/start - это сообщение\n"
        f"/menu - главное меню\n"
        f"/help - помощь\n\n"
        f"<i>Бот работает на бесплатном тарифе Bothost</i> ✅"
    )
    
    # Логируем
    logger.info(f"Пользователь {user.id} ({user.first_name}) запустил бота")

# /menu - главное меню с кнопками
async def menu(update: Update, context: CallbackContext):
    # Создаём клавиатуру
    keyboard = [
        ["🚗 Добавить машину"],
        ["📊 Прогресс смены", "📜 История"],
        ["⚙️ Настройки", "❓ Помощь"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    await update.message.reply_text(
        "📱 <b>Главное меню</b>\n\n"
        "Выберите действие:",
        reply_markup=reply_markup,
        parse_mode='HTML'
    )

# Обработка кнопок
async def handle_buttons(update: Update, context: CallbackContext):
    text = update.message.text
    
    if text == "🚗 Добавить машину":
        await update.message.reply_text(
            "Введите номер машины (например, <code>А123БВ777</code>):",
            parse_mode='HTML'
        )
    
    elif text == "📊 Прогресс смены":
        await update.message.reply_text(
            "📊 <b>Прогресс смены</b>\n\n"
            "Смена ещё не начата.\n"
            "Начните смену через меню настроек.",
            parse_mode='HTML'
        )
    
    elif text == "📜 История":
        await update.message.reply_text(
            "История смен будет здесь.\n"
            "Функция в разработке... 🛠️"
        )
    
    elif text == "⚙️ Настройки":
        await update.message.reply_text(
            "⚙️ <b>Настройки</b>\n\n"
            "1. Установить цель на смену\n"
            "2. Включить уведомления\n"
            "3. Сменить имя\n\n"
            "Функции в разработке... 🛠️",
            parse_mode='HTML'
        )
    
    elif text == "❓ Помощь":
        await update.message.reply_text(
            "🆘 <b>Помощь</b>\n\n"
            "Это бот для учёта услуг.\n\n"
            "Как работать:\n"
            "1. Начните смену (/menu → Настройки)\n"
            "2. Добавляйте машины\n"
            "3. Выбирайте услуги\n"
            "4. Закрывайте смену\n\n"
            "Связь: @ваш_username",
            parse_mode='HTML'
        )

# Обработка номера машины
async def handle_car_number(update: Update, context: CallbackContext):
    car_number = update.message.text.upper().strip()
    
    # Простая проверка
    if len(car_number) < 6:
        await update.message.reply_text("❌ Номер слишком короткий!")
        return
    
    await update.message.reply_text(
        f"🚗 Машина: <b>{car_number}</b>\n\n"
        f"Выберите услуги (скоро появятся inline-кнопки):\n\n"
        f"1. Проверка - 150₽\n"
        f"2. Заправка - 300₽\n"
        f"3. Подкачка - 80₽\n\n"
        f"<i>Inline-кнопки в разработке...</i>",
        parse_mode='HTML'
    )
    
    # Сохраняем номер в контексте
    context.user_data['last_car'] = car_number

# /help - помощь
async def help_command(update: Update, context: CallbackContext):
    await update.message.reply_text(
        "ℹ️ <b>Информация о боте</b>\n\n"
        "Версия: 1.0 (базовая)\n"
        "Статус: В разработке\n"
        "Хостинг: Bothost (бесплатный тариф)\n\n"
        "Следующие обновления:\n"
        "✅ Inline-кнопки с услугами\n"
        "✅ Прогресс-бар в закреплённых\n"
        "✅ База данных\n\n"
        "Ожидайте обновлений!",
        parse_mode='HTML'
    )

# ========== ЗАПУСК БОТА ==========

def main():
    """Главная функция запуска бота"""
    logger.info("=" * 50)
    logger.info("ЗАПУСК БОТА ДЛЯ БЕСПЛАТНОГО ТАРИФА")
    logger.info("=" * 50)
    
    try:
        # Создаём приложение
        application = Application.builder().token(config.BOT_TOKEN).build()
        
        # Регистрируем команды
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("menu", menu))
        application.add_handler(CommandHandler("help", help_command))
        
        # Обработчики сообщений
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_buttons))
        
        # Обработчик ошибок
        async def error_handler(update: Update, context: CallbackContext):
            logger.error(f"Ошибка: {context.error}")
        
        application.add_error_handler(error_handler)
        
        # Запускаем бота
        logger.info(f"Бот запускается с токеном: {config.BOT_TOKEN[:10]}...")
        logger.info("Используется polling (подходит для бесплатного тарифа)")
        
        application.run_polling(
            drop_pending_updates=True,
            allowed_updates=Update.ALL_TYPES
        )
        
    except Exception as e:
        logger.error(f"ФАТАЛЬНАЯ ОШИБКА: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
