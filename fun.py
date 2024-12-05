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
