import sqlite3

DATABASE_PATH = 'app_database.db'


def register_user(log, emal, pas):
    try:
        with sqlite3.connect(DATABASE_PATH) as conn:
            cursor = conn.cursor()

            # Проверка существования пользователя
            cursor.execute("SELECT 1 FROM my_table WHERE loggin = ? LIMIT 1", (log,))
            if cursor.fetchone():
                return False  # Пользователь уже существует

            # Регистрация нового пользователя
            cursor.execute('''
                INSERT INTO my_table (loggin, email, address) VALUES (?, ?, ?)
            ''', (log, emal, pas))


            return True
    except sqlite3.Error as e:

        return False


def authenticate_user(log, pas):
    try:
        with sqlite3.connect(DATABASE_PATH) as conn:
            cursor = conn.cursor()

            # Ищем пользователя по логину
            cursor.execute("SELECT address FROM my_table WHERE loggin = ?", (log,))
            result = cursor.fetchone()

            if result and result[0] == pas:  # Проверка пароля
                return {"status": "success", "message": "User authenticated"}
            return None
    except sqlite3.Error as e:

        return None
