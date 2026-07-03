from flask import Flask, render_template, request, redirect, url_for
from data_manager import DataManager
from models import db
from api.api_call import get_movie_by_name
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
os.makedirs(os.path.join(basedir, 'data'), exist_ok=True)

app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'data', 'library.sqlite')}"

db.init_app(app)

data_manager = DataManager()


@app.route('/')
@app.route('/index', methods=['GET'])
def index():
    users = data_manager.get_users()
    return render_template('index.html', users=users)


@app.route('/users', methods=['GET'])
def users():
    users = data_manager.get_users()
    return render_template('users.html', users=users)


@app.route('/add_user', methods=['GET'])
def add_user_form():
    return render_template('add_user.html')


@app.route('/add_user', methods=['POST'])
def add_user():
    name = request.form.get('name')
    if name:
        data_manager.create_user(name)
    return redirect(url_for('success', message=f'User "{name}" added.'))


@app.route('/users/<int:user_id>/movies', methods=['GET'])
def movies(user_id):
    user = data_manager.get_user(user_id)
    movies = data_manager.get_movies(user_id)
    return render_template('index.html', movies=movies, user=user, users=data_manager.get_users())


@app.route('/users/<int:user_id>/add_movie', methods=['GET'])
def add_movie_form(user_id):
    user = data_manager.get_user(user_id)
    return render_template('add_movie.html', user=user)


@app.route('/users/<int:user_id>/movies', methods=['POST'])
def add_movie(user_id):
    title = request.form.get('title')
    omdb_data = get_movie_by_name(title) if title else None

    if omdb_data:
        director = omdb_data.get('Director')
        year = omdb_data.get('Year')
        try:
            year = int(str(year)[:4])
        except (ValueError, TypeError):
            year = None
        poster_url = omdb_data.get('Poster')
        title = omdb_data.get('Title', title)
    else:
        director = request.form.get('director')
        year = request.form.get('year') or None
        poster_url = request.form.get('poster_url')

    data_manager.add_movie(user_id, title, director, year, poster_url)
    return redirect(url_for('success', message=f'Movie "{title}" added.', user_id=user_id))


@app.route('/users/<int:user_id>/movies/<int:movie_id>', methods=['GET'])
def movie_details(user_id, movie_id):
    movie = data_manager.get_movie(movie_id)
    return render_template('movie_details.html', movie=movie, user_id=user_id)


@app.route('/users/<int:user_id>/movies/<int:movie_id>/update', methods=['POST'])
def update_movie(user_id, movie_id):
    data_manager.update_movie(movie_id, request.form)
    return redirect(url_for('success', message='Movie updated.', user_id=user_id))


@app.route('/users/<int:user_id>/movies/<int:movie_id>/delete', methods=['POST'])
def delete_movie(user_id, movie_id):
    data_manager.delete_movie(movie_id)
    return redirect(url_for('success', message='Movie deleted.', user_id=user_id))


@app.route('/success', methods=['GET'])
def success():
    message = request.args.get('message', 'Done!')
    user_id = request.args.get('user_id')
    return render_template('success.html', message=message, user_id=user_id)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)