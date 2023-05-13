# Импортируем необходимые библиотеки
import pandas as pd
import sqlite3

# Задаем имя файла excel и базы данных
excel_file = "../school.xlsx"
db_file = "../school.db"

# Спрашиваем пользователя, какие страницы excel-файла добавить в базу данных
sheets = (input("Введите названия страниц excel-файла через запятую: ").split(","))

for sheet in sheets:
    # Удаляем пробелы по бокам
    sheet = sheet.strip().lower()
    # Считываем данные из excel-файла в датафрейм
    df = pd.read_excel(excel_file, sheet_name=sheet, dtype=str)
    # Создаем подключение к базе данных
    conn = sqlite3.connect(db_file)
    # Записываем датафрейм в таблицу в базе данных с именем страницы excel-файла и указанным типом данных TEXT для всех полей
    df.to_sql(sheet, conn, if_exists='replace')
    # Закрываем соединение с базой данных
    conn.close()
    # Выводим сообщение об успешном завершении программы
    print(f"Таблица {sheet} создана в базе данных {db_file}.")