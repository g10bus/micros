from flask import Flask, jsonify, request
import sqlite3
import fun

app = Flask(__name__)


@app.route('/', methods=['GET'])
def greet():
    naznach = request.args.get('purpose')
    login = request.args.get('login')
    email = request.args.get('email')
    password = request.args.get('password')

    if naznach == "Registr":
        result = fun.register_user(login, email, password)
        if result:
            return jsonify({"status": "success", "message": f"Пользователь {login} зарегистрирован"})
        else:
            return jsonify({"status": "error", "message": "Пользователь уже существует или ошибка базы данных"}), 400

    elif naznach == "Auth":
        result = fun.authenticate_user(login, password)
        if result:
            return jsonify(result)
        else:
            return jsonify({"status": "error", "message": "Неверные учетные данные"}), 401

    return jsonify({"status": "error", "message": "Неверное значение purpose"}), 400


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
