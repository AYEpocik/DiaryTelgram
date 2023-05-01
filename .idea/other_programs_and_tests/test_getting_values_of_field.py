import sqlite3


DB_PATH = '../../Database/school.db'

def get_values_of_field(table: str, field: str) -> list:
    request = f'SELECT {field} FROM {table}'
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(request)
        list_of_values = cursor.fetchall()
    for i in range(len(list_of_values)):
        list_of_values[i] = list_of_values[i][0]
    #list_of_values = list(list_of_values[0])
    list_of_values = list(filter(None,list_of_values))
    return list_of_values

print(get_values_of_field('users', 'user_id'))