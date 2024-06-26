from flask import Flask, request, render_template
import sqlite3

# Инициализация Flask приложения
app = Flask(__name__)

# Создание соединения с базой данных
con = sqlite3.connect('new.db', check_same_thread=False)
# Создание курсора для выполнения SQL запросов
cur = con.cursor()

# Маршрут для корневой страницы
@app.route("/")
def hello_world():
    # Возвращение приветственного сообщения
    return render_template('main.html')

# Маршрут для получения информации о фильме по ID
@app.route("/film/<id>")
def film(id):
    # Выполнение SQL запроса для получения данных о фильме по ID
    res = cur.execute(f"select * from Movies where id = ?", (id,))
    # Получение результата запроса
    films = res.fetchone()
    # Проверка, найден ли фильм
    if films != None:
        # Формирование строки с информацией о фильме
        t = f"ID {films[0]}, Название: {films[1]}, Год выпуска: {films[2]} "
    else:
        # Сообщение о том, что фильма не существует
        t = "Такого фильма нет"
    # Возвращение результата
    return t

@app.route("/films")
def films():
    return render_template('film.html')

# Маршрут для добавления нового фильма
@app.route("/film_add")
def film_add():
    # Получение данных о фильме из параметров запроса
    name = request.args.get('name')
    genre = request.args.get('genre')
    year = request.args.get('year')
    rating = request.args.get('rating')
    # Формирование кортежа с данными о фильме
    film_data = (name, genre, year, rating)
    # Выполнение SQL запроса для добавления фильма в базу данных
    cur.execute('INSERT INTO Movies (name, genre, year, rating) VALUES (?, ?, ?, ?)', film_data)
    # Сохранение изменений в базе данных
    con.commit()
    # Возвращение подтверждения о добавлении фильма
    return "name = {};genre = {}; year = {}; rating = {} ".format(name, genre, year, rating) 

# Запуск приложения, если оно выполняется как главный модуль
if __name__ == '__main__':
    app.run(debug=True)
