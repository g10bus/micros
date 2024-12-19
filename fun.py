import os
import sqlite3

DATABASE_PATH = 'app_database.db'


def register_user(log, emal, pas):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    try:
        # Проверка существования пользователя
        cursor.execute("SELECT * FROM my_table WHERE loggin = ?", (log,))
        if cursor.fetchone():
            return False  # Пользователь уже существует

        # Регистрация нового пользователя
        cursor.execute('''
            INSERT INTO my_table (loggin, email, address) VALUES (?, ?, ?)
        ''', (log, emal, pas))

        conn.commit()
        print("ok Registr")
        return True
    except sqlite3.Error as e:
        print(f"Ошибка базы данных при регистрации: {e}")
        return False
    finally:
        conn.close()


def authenticate_user(log, pas):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    try:
        # Ищем пользователя по логину
        cursor.execute("SELECT * FROM my_table WHERE loggin = ?", (log,))
        user = cursor.fetchone()

        if user and user[3] == pas:  # Проверка пароля
            return {"status": "success", "message": "User authenticated"}
        else:
            return None
    except sqlite3.Error as e:
        print(f"Ошибка базы данных при аутентификации: {e}")
        return None
    finally:
        conn.close()

def add_recipe(title, description, image_path, author):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    try:
        image_filename = os.path.basename(image_path)
        cursor.execute('''
            INSERT INTO recipes (title, description, image_path, author)
            VALUES (?, ?, ?, ?)
        ''', (title, description, image_filename, author))
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"Ошибка базы данных: {e}")
        return False
    finally:
        conn.close()


def get_all_recipes():
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM recipes")
        rows = cursor.fetchall()
        base_url = "http://10.19.30.54:5000/uploads/"
        return [
            {"id": row[0], "title": row[1],
             "description": row[2],
             "image_path": base_url + row[3], # Генерация URL для изображения
             "author": row[4]}
            for row in rows
        ]
    except sqlite3.OperationalError as e:
        print(f"Ошибка базы данных: {e}")
        return []  # Возвращает пустой список, чтобы избежать краха
    finally:
        conn.close()