from flask import Flask, request, render_template
import sqlite3
from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import DataRequired

# Определение формы для добавления фильма
class MyForm(FlaskForm):
    # Поле для названия фильма
    name = StringField('Название', validators=[DataRequired()]) 
    # Поле для года выпуска фильма
    year = IntegerField('Год выпуска')
    # Поле для рейтинга фильма
    rating = FloatField('Рейтинг')
    # Поле для жанра фильма
    genre = StringField('Жанр')

# Инициализация Flask приложения
app = Flask(__name__)

# Создание соединения с базой данных
con = sqlite3.connect('films.db', check_same_thread=False)
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
    film = res.fetchone()
    print(film)
    # Проверка, найден ли фильм
    if film != None:
        # Возвращение результата
        return render_template('film.html', film = film )
    else:
        # Сообщение о том, что фильма не существует   
        return "Такого фильма нет"

# Маршрут для получения списка всех фильмов
@app.route("/films" )
def films():
    # Выполнение SQL запроса для получения всех фильмов
    res = cur.execute("select * from Movies")
    # Получение результата запроса
    films = res.fetchall()
    # Возвращение списка фильмов
    return render_template('films.html', films = films)

# Маршрут для отображения формы добавления фильма
@app.route("/film_form", methods=['GET', 'POST'])
def film_form():
    # Создание формы
    form = MyForm()
    # Проверка, была ли отправлена заполненная форма на сервер
    if form.validate_on_submit():
        # Если форма была отправлена, выводим сообщение о том, что форма отправлена
        # todo: разобрать данные с формы здесь
        return 'Данные отправлены на сервер!'
    # Возвращаем форму для отображения к заполнению
    return render_template('form.html', form=form)

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
    # Отключение проверки CSRF для WTForms
    app.config["WTF_CSRF_ENABLED"] = False  
    # Запуск приложения в режиме отладки
    app.run(debug=True)
