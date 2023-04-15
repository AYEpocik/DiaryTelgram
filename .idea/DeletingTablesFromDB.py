# Импортируем модуль sqlite3
import sqlite3

# Указываем путь к файлу базы данных
DB_PATH = input('Введите путь к базе данных: ')[1:-1]

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
    # Спрашиваем пользователя, хочет ли он удалить таблицу
    answer = input(f"Do you want to delete the table {table_name}? (y/n) ")
    # Если пользователь ответил да
    if answer.lower() == "y":
        # Удаляем таблицу из базы данных
        cursor.execute(f"DROP TABLE {table_name}")
        # Выводим сообщение об успешном удалении
        print(f"Table {table_name} deleted successfully.")
    # Иначе
    else:
        # Выводим сообщение о пропуске таблицы
        print(f"Table {table_name} skipped.")

# Сохраняем изменения в базе данных
conn.commit()
# Закрываем соединение с базой данных
conn.close()