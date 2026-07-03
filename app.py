from flask import Flask, render_template, request, redirect, url_for, abort, flash
from sqlalchemy.exc import SQLAlchemyError

from data_manager import DataManager
from models import db
from api.api_call import get_movie_by_name
import os
import logging

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
os.makedirs(os.path.join(basedir, 'data'), exist_ok=True)

app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'data', 'library.sqlite')}"

db.init_app(app)

data_manager = DataManager()

# Error handling

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s'
)
logger = logging.getLogger(__name__)

@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('404.html'), 500


@app.errorhandler(SQLAlchemyError)
def handle_db_error(e):
    logger.error("unexpected database error: %s", e)
    return render_template('404.html'), 500

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
    name = request.form.get('name', '').strip()
    if not name:
        return redirect(url_for('add_user_form', error='Please enter a name.'))

    data_manager.create_user(name)
    return redirect(url_for('success', message=f'User "{name}" added.'))


@app.route('/users/<int:user_id>/movies', methods=['GET'])
def movies(user_id):
    user = data_manager.get_user(user_id)
    if user is None:
        abort(404)

    movies = data_manager.get_movies(user_id)
    return render_template('index.html', movies=movies, user=user, users=data_manager.get_users())


@app.route('/users/<int:user_id>/add_movie', methods=['GET'])
def add_movie_form(user_id):
    user = data_manager.get_user(user_id)
    if user is None:
        abort(404)
    return render_template('add_movie.html', user=user)


@app.route('/users/<int:user_id>/movies', methods=['POST'])
def add_movie(user_id):
    user = data_manager.get_user(user_id)
    if user is None:
        abort(404)

    title = request.form.get('title', '').strip()
    if not title:
        return redirect(url_for('add_movie_form', user_id=user_id, error='Please enter a movie name.'))

    omdb_data = get_movie_by_name(title)
    omdb_notice = None

    if omdb_data:
        director = omdb_data.get('Director')
        year_raw = omdb_data.get('Year')
        poster_url = omdb_data.get('Poster')
        title = omdb_data.get('Title', title)
    else:
        director = request.form.get('director') or None
        year_raw = request.form.get('year')
        poster_url = request.form.get('poster_url') or None
        omdb_notice = f'"{title}" was not found, manually entered data will be added.'

    try:
        year = int(str(year_raw)[:4]) if year_raw else None
    except (ValueError, TypeError):
        year = None
        logger.warning("Invalid year", year_raw, title)

    data_manager.add_movie(user_id, title, director, year, poster_url)
    message = omdb_notice or f'Movie "{title}" added.'
    return redirect(url_for('success', message=message, user_id=user_id))


@app.route('/users/<int:user_id>/movies/<int:movie_id>', methods=['GET'])
def movie_details(user_id, movie_id):
    movie = data_manager.get_movie(movie_id)
    if movie is None or movie.user_id != user_id:
        abort(404)

    return render_template('movie_details.html', movie=movie, user_id=user_id)


@app.route('/users/<int:user_id>/movies/<int:movie_id>/update', methods=['POST'])
def update_movie(user_id, movie_id):
    updated = data_manager.update_movie(movie_id, request.form)
    if updated is None:
        abort(404)

    return redirect(url_for('success', message='Movie updated.', user_id=user_id))


@app.route('/users/<int:user_id>/movies/<int:movie_id>/delete', methods=['POST'])
def delete_movie(user_id, movie_id):
    deleted = data_manager.delete_movie(movie_id)
    if not deleted:
        abort(404)

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