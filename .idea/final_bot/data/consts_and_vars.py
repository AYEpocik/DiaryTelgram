import os
import sqlite3 # Импортируем библиотеку для работы с базой данных


# Определяем токен "schoolhelper_bot"-а
TOKEN = '6111962134:AAHxMHk9M44KTy7I_ZL9fSXYKOL2Cw3n-W8'

# Определяем путь к файлу с базой данных
DB_PATH = '../../Database/school.db'

# Определяем путь к папке с анекдотами
JOKES_PATH = r'../../../Database/jokes'
def abs_path(FILE_PATH: str) -> str:
    # Получаем абсолютный путь к текущей директории
    current_dir = os.path.abspath(os.path.dirname(__file__))
    # Соединяем абсолютный путь к текущей директории с относительным путем к файлу
    full_path = os.path.join(current_dir, FILE_PATH)
    # Нормализуем путь, убирая лишние символы
    full_path = os.path.normpath(full_path)
    return full_path

# Словарь с переводами названий предметов
school_subjects = {
    'Русский': 'russian',
    'Профиль': 'profmath',
    'База': 'basemath',
    'Физика': 'physics',
    'Химия': 'chemistry',
    'Биология': 'biology',
    'История': 'history',
    'География': 'geography',
    'Английский': 'english',
    'Общество': 'society',
    'Литература': 'literature',
    'Информатика': 'informatics',
    'Немецкий': 'german',
    'Французский': 'french',
    'Испанский': 'spanish',
    'Китайский': 'chinese'
}


# Словарь с предметами в дательном падеже
school_subjects_in_dp = {
    'russian': 'по русскому языку',
    'profmath': 'по профильной математике',
    'basemath': 'по базовой математике',
    'physics': 'по физике',
    'chemistry': 'по химии',
    'informatics': 'по информатике',
    'biology': 'по биологии',
    'history': 'по истории',
    'geography': 'по географии',
    'english': 'по английскому языку',
    'german': 'по немецкому языку',
    'french': 'по французскому языку',
    'society': 'по обществознанию',
    'spanish': 'по испанскому языку',
    'chinese': 'по китайскому языку',
    'literature': 'по литературе'
}

# Словарь с переводами дней недели
weekdays = {
    'monday': 'понедельник',
    'tuesday': 'вторник',
    'wednesday': 'среда',
    'thursday': 'четверг',
    'friday': 'пятница',
    'saturday': 'суббота'
}

# Словарь с Винительными Падежами дней недели (для кнопки "Что в столовой?")
weekdays_in_vp = {
    'monday': 'В понедельник',
    'tuesday': 'Во вторник',
    'wednesday': 'В среду',
    'thursday': 'В четверг',
    'friday': 'В пятницу',
    'saturday': 'В субботу'
}

def all_surnames(DB_PATH=DB_PATH) -> list:
    request = 'SELECT surname FROM monday'
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(request)
        surnames = cursor.fetchall()
        for i in range(len(surnames)):
            surnames[i] = surnames[i][0]
    return surnames

def get_second_scores(subject: str, DB_PATH=DB_PATH) -> list:
    request = f"SELECT * FROM scores WHERE subject = '{subject}'"
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(request)
        sec_scores = cursor.fetchall()
    for i in range(len(sec_scores)):
        sec_scores[i] = sec_scores[i][3:]
    sec_scores = list(sec_scores[0])
    sec_scores = list(filter(None,sec_scores))
    for i in range(len(sec_scores)):
        sec_scores[i] = int(sec_scores[i])
    return sec_scores

def list_of_values(table: str, field: str, row_value: str, DB_PATH=DB_PATH) -> list:
    request = f"SELECT * FROM {table} WHERE {field} = '{row_value}'"
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(request)
        list_of_values = cursor.fetchall()
    for i in range(len(list_of_values)):
        list_of_values[i] = list_of_values[i][2:]
    list_of_values = list(list_of_values[0])
    list_of_values = list(filter(None,list_of_values))
    return list_of_values

def first_to_second(subject: str, first_score: int) -> int:
    second_score = get_second_scores(subject)[first_score-1]
    return second_score
