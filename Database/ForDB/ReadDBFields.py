# Импортируем модуль sqlite3
import sqlite3

# Указываем путь к файлу базы данных
DB_PATH = '../../Database/school.db'

# Подключаемся к базе данных
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Получаем список всех таблиц в базе данных
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()

# Для каждой таблицы в базе данных
for table in tables:
    # Получаем имя таблицы
    table_name = table[0]
    # Выводим имя таблицы на экран
    print(f"Table: '{table_name}' ")
    # Получаем список всех полей в таблице
    cursor.execute(f"PRAGMA table_info({table_name})")
    fields = cursor.fetchall()
    # Для каждого поля в таблице
    for field in fields:
        # Получаем имя поля
        field_name = field[1]
        # Выводим имя поля на экран с отступом
        print(f"  Field: '{field_name}'")
    # Выводим пустую строку для разделения таблиц
    print()

# Закрываем соединение с базой данных
conn.close()