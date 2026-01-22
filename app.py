"""
Точка входа для Bothost.
Bothost ищет приложение в переменной 'app'
"""
import asyncio
import os
import sys

# Добавляем текущую директорию в путь
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from main import app, handle_webhook
    print("✅ Модули успешно импортированы")
    
    # Проверяем, что приложение создано
    if app is None:
        print("❌ Приложение не создано!")
        sys.exit(1)
        
    print(f"✅ Бот готов: {app.bot.first_name}")
    
except Exception as e:
    print(f"❌ Ошибка импорта: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Bothost будет использовать эту функцию
async def handler(request):
    return await handle_webhook(request)
