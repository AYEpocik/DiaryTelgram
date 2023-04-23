# Импортируем модули
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# Указываем путь к базе данных
DB_PATH = "../Database/school.db"

def surnames(DB_PATH=DB_PATH):
    # Устанавливаем соединение с базой данных
    conn = sqlite3.connect(DB_PATH)
    # Создаем курсор
    cursor = conn.cursor()
    # Формируем запрос
    query = "SELECT surname FROM monday"
    # Выполняем запрос
    cursor.execute(query)
    # Получаем результаты
    results = cursor.fetchall()
    # Создаем пустой список
    surnames = []
    # Перебираем результаты и добавляем их в список
    for row in results:
        surnames.append(row[0])
    # Преобразуем список в кортеж
    surnames = tuple(surnames)
    # Закрываем курсор и соединение
    cursor.close()
    conn.close()
    return surnames

# Запрашиваем фамилию
surname = input('Введите фамилию ученика: ').lower()
while surname not in surnames():
    surname = input('Такой ученик не найден. Попробуйте еще раз: ').lower()

def create_week_schedule(surname, DB_PATH):
    # Создаем подключение к базе данных
    conn = sqlite3.connect(DB_PATH)
    # Задаем путь для сохранения изображения расписания
    output_path = f'../Schedules/{surname}.jpg'
    # Создаем пустой датафрейм для хранения расписания
    schedule = pd.DataFrame()
    # Список дней недели
    days = {"monday":"Понедельник", "tuesday":"Вторник", "wednesday":"Среда", "thursday":"Четверг", "friday":"Пятница"}
    # Цикл по дням недели
    for day in days:
        # Запрос к базе данных для выбора уроков ученика по фамилии
        query = f"SELECT * FROM {day} WHERE surname = '{surname}'"
        # Выполняем запрос и получаем результат в виде датафрейма
        df = pd.read_sql_query(query, conn)
        # Удаляем столбцы с индексом и фамилией
        df.drop(["index", "surname"], axis=1, inplace=True)
        # Транспонируем датафрейм, чтобы строки соответствовали номерам уроков
        df = df.T
        # Переименовываем столбец с уроками в название дня недели
        df.rename(columns={0: days[day]}, inplace=True)
        #df = vert_rearrange_columns(df, 3)
        # Добавляем датафрейм к общему расписанию без параметра fill_value
        schedule = pd.concat([schedule, df], axis=1)
    # Сохраняем расписание в jpg-файл
    plt.figure(figsize=(13, 2), dpi=1000)
    plt.table(cellText=schedule.values, colLabels=schedule.columns, cellLoc="left", loc='upper left')
    plt.axis("off")
    plt.savefig(output_path, dpi=1000)
    # Закрываем соединение с базой данных
    conn.close()

# Запускаем выполнение функции
create_week_schedule(surname, DB_PATH)
