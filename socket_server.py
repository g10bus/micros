from flask import Flask, jsonify, request
import sqlite3
import fun  # Ваш модуль с функциями регистрации и аутентификации

app = Flask(__name__)


@app.route('/greet', methods=['GET'])
def greet():
    # Получаем параметры из запроса
    purpose = request.args.get('purpose')
    login = request.args.get('login')
    email = request.args.get('email')
    password = request.args.get('password')

    # Проверка обязательных параметров
    if not login or not password or not purpose:
        return jsonify({"status": "error", "message": "Поля purpose, login и password обязательны"}), 400

    if purpose == "Registr":
        return handle_registration(login, email, password)
    elif purpose == "Auth":
        return handle_authentication(login, password)
    else:
        return jsonify({"status": "error", "message": "Неверное значение purpose"}), 400


def handle_registration(login, email, password):
    """Обработка запроса на регистрацию."""
    result = fun.register_user(login, email, password)
    if result:  # Регистрация успешна
        return jsonify({"status": "success", "message": f"Пользователь {login} зарегистрирован"})
    else:
        return jsonify({"status": "error", "message": "Пользователь уже существует или ошибка базы данных"}), 400


def handle_authentication(login, password):
    """Обработка запроса на аутентификацию."""
    result = fun.authenticate_user(login, password)
    if result:  # Аутентификация успешна
        return jsonify(result)
    else:
        return jsonify({"status": "error", "message": "Неверные учетные данные"}), 401


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
