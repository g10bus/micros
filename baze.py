import sqlite3

# Создаем или открываем базу данных
conn = sqlite3.connect('app_database.db')

# Создаем объект курсора для выполнения SQL-запросов
cursor = conn.cursor()

def update_table_structure():
    conn = sqlite3.connect('app_database.db')
    cursor = conn.cursor()
    try:
        # Добавление новых столбцов (если их ещё нет)
        cursor.execute("ALTER TABLE recipes ADD COLUMN timeCook TEXT")
        cursor.execute("ALTER TABLE recipes ADD COLUMN countPortions TEXT")
        cursor.execute("ALTER TABLE recipes ADD COLUMN ingredients TEXT")
        print("Структура таблицы обновлена.")
    except sqlite3.OperationalError as e:
        # Если столбец уже существует, будет выброшено исключение, которое мы можем игнорировать
        if "duplicate column name" in str(e).lower():
            print("Столбец уже существует. Обновление не требуется.")
        else:
            print(f"Ошибка при обновлении таблицы: {e}")
    finally:
        conn.close()

# Вызов функции
update_table_structure()

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
    author TEXT NOT NULL,
    timeCook TEXT NOT NULL,
    countPortions TEXT NOT NULL,
    ingredients TEXT NOT NULL
)
''')

# Применяем изменения и закрываем соединение
conn.commit()
conn.close()

print("Инициализация базы данных завершена успешно.")
