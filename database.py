import psycopg2
import logging
from config import DATABASE_URL

logger = logging.getLogger(__name__)

def create_tables():
    """Создаём таблицы в базе данных"""
    commands = (
        """
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            telegram_id BIGINT UNIQUE NOT NULL,
            name VARCHAR(100) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS services (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            day_price DECIMAL(10,2) NOT NULL,
            night_price DECIMAL(10,2) NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS shifts (
            id SERIAL PRIMARY KEY,
            user_id INTEGER REFERENCES users(id),
            start_time TIMESTAMP NOT NULL,
            end_time TIMESTAMP,
            total_amount DECIMAL(10,2) DEFAULT 0,
            status VARCHAR(20) DEFAULT 'active'
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS cars (
            id SERIAL PRIMARY KEY,
            shift_id INTEGER REFERENCES shifts(id),
            car_number VARCHAR(20) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(shift_id, car_number)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS work_logs (
            id SERIAL PRIMARY KEY,
            car_id INTEGER REFERENCES cars(id),
            service_id INTEGER REFERENCES services(id),
            quantity INTEGER DEFAULT 1,
            performed_at TIMESTAMP NOT NULL,
            amount DECIMAL(10,2) NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS user_settings (
            user_id INTEGER PRIMARY KEY REFERENCES users(id),
            progress_bar_enabled BOOLEAN DEFAULT TRUE,
            daily_target DECIMAL(10,2) DEFAULT 5000.00,
            auto_reports_enabled BOOLEAN DEFAULT TRUE
        )
        """
    )
    
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        
        for command in commands:
            cur.execute(command)
        
        conn.commit()
        cur.close()
        conn.close()
        logger.info("Таблицы успешно созданы")
        
    except Exception as e:
        logger.error(f"Ошибка при создании таблиц: {e}")
