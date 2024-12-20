from flask import Flask, jsonify, request, send_from_directory
import sqlite3
import fun
import os

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Директория, где находится socket_server.py
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
print(f"BASE_DIR: {BASE_DIR}")
print(f"UPLOAD_FOLDER: {UPLOAD_FOLDER}")

try:
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
        print(f"Папка {UPLOAD_FOLDER} создана успешно.")
    else:
        print("Папка уже существует.")
except Exception as e:
    print(f"Ошибка при создании папки: {e}")

@app.route('/greet', methods=['GET'])
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



@app.route('/upload_recipe', methods=['POST'])
def upload_recipe():
    try:
        if 'image' not in request.files:
            return jsonify({"status": "error", "message": "Изображение не загружено"}), 400

        image = request.files['image']
        title = request.form.get('title')
        description = request.form.get('description')
        author = request.form.get('author')
        timeCook = request.form.get('timeCook')
        countPortions = request.form.get('countPortions')
        ingredients = request.form.get('ingredients')

        print(
            f"title: {title}, description: {description}, author: {author}, timeCook: {timeCook}, servings: {countPortions}, ingredients: {ingredients}")

        # Проверка на заполнение всех полей
        if not (title and description and author and timeCook and countPortions and ingredients):
            return jsonify({"status": "error", "message": "Все поля должны быть заполнены"}), 400

        # Проверяем наличие папки uploads
        UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
        if not os.path.exists(UPLOAD_FOLDER):
            os.makedirs(UPLOAD_FOLDER)

        # Путь сохранения изображения
        image_path = os.path.join(UPLOAD_FOLDER, image.filename)
        image.save(image_path)

        # # Сохраняем изображение в папку uploads
        # image_path = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
        # image.save(image_path)

        # # Формируем URL для доступа к изображению
        # image_url = request.url_root + 'uploads/' + image.filename

        # Сохранение данных рецепта в базе данных
        result = fun.add_recipe(title, description, image_path, author, timeCook, countPortions, ingredients)
        if result:
            return jsonify({"status": "success", "message": "Рецепт загружен"}), 200
        else:
            return jsonify({"status": "error", "message": "Ошибка базы данных"}), 500

    except Exception as e:
        return jsonify({"status": "error", "message": f"Ошибка сохранения изображения: {e}"}), 500
#Прошлые изменения
    # result = fun.add_recipe(title, description, image_path, author)
    # if result:
    #     return jsonify({"status": "success", "message": "Рецепт загружен"}), 200
    # else:
    #     return jsonify({"status": "error", "message": "Ошибка базы данных"}), 500




#Новые изменения
# @app.route('/uploads/<filename>', methods=['GET'])
# def uploaded_file(filename):
#     try:
#         return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
#     except Exception as e:
#         return jsonify({"status": "error", "message": f"Ошибка доступа к файлу: {e}"}), 404


@app.route('/get_recipes', methods=['GET'])
def get_recipes():
    try:
        recipes = fun.get_all_recipes()
        return jsonify({"status": "success", "recipes": recipes}), 200

    except Exception as e:
        print(f"Ошибка при получении рецептов: {e}")
        return jsonify({"status": "error", "message": "Ошибка базы данных"}), 500

@app.route('/uploads/<filename>', methods=['GET'])
def uploaded_file(filename):
    try:
        return send_from_directory(UPLOAD_FOLDER, filename)
    except Exception as e:
        return jsonify({"status": "error", "message": f"Ошибка доступа к файлу: {e}"}), 404



if __name__ == '__main__':
    # Создаём папку перед запуском сервера
    if not os.path.exists(UPLOAD_FOLDER):
        try:
            os.makedirs(UPLOAD_FOLDER)
            print(f"Папка {UPLOAD_FOLDER} создана успешно.")
        except Exception as e:
            print(f"Ошибка при создании папки {UPLOAD_FOLDER}: {e}")
    app.run(host='0.0.0.0', port=5000)
