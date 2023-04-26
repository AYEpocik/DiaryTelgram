# Определяем токен "schoolhelper_bot"-а
TOKEN = '6111962134:AAHxMHk9M44KTy7I_ZL9fSXYKOL2Cw3n-W8'

# Определяем путь к файлу с базой данных
DB_PATH = "../../Database/school.db"

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

# Словарь с переводами дней недели
weekdays = {'monday':'Понедельник',
            'tuesday':'Вторник',
            'wednesday':'Среда',
            'thursday':'Четверг',
            'friday':'Пятница',
            'saturday':'Суббота'
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