# Импортируем необходимые библиотеки
import pandas as pd
import sqlite3

# Задаем имя файла excel и базы данных
excel_file = "../Database/school.xlsx"
db_file = "../Database/school.db"

# Спрашиваем пользователя, какую страницу excel-файла добавить в базу данных
sheet_name = input("Введите название страницы excel-файла: ")

# Считываем данные из excel-файла в датафрейм
df = pd.read_excel(excel_file, sheet_name=sheet_name, dtype=str)

# Создаем подключение к базе данных
conn = sqlite3.connect(db_file)

# Записываем датафрейм в таблицу в базе данных с именем страницы excel-файла и указанным типом данных TEXT для всех полей
df.to_sql(sheet_name, conn, if_exists="replace")

# Закрываем соединение с базой данных
conn.close()

# Выводим сообщение об успешном завершении программы
print(f"Программа завершена. Данные из файла {excel_file} добавлены в таблицу {sheet_name} в базе данных {db_file}.")