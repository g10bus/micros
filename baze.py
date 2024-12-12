import sqlite3

# Создаем или открываем базу данных
conn = sqlite3.connect('app_database.db')

# Создаем объект курсора для выполнения SQL-запросов
cursor = conn.cursor()

# Создаем таблицу пользователей
cursor.execute('''
CREATE TABLE IF NOT EXISTS my_table (
    id INTEGER PRIMARY KEY,
    loggin TEXT NOT NULL,
    email TEXT NOT NULL,
    address TEXT NOT NULL
)
''')

# Создаем таблицу рецептов
cursor.execute('''
CREATE TABLE IF NOT EXISTS recipes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    image_path TEXT NOT NULL,
    author TEXT NOT NULL
)
''')

# Применяем изменения и закрываем соединение
conn.commit()
conn.close()

print("Инициализация базы данных завершена успешно.")
