from models import db, User, Movie


class DataManager:
    """Handles all database read/write operations for Users and Movies."""

    def create_user(self, name):
        new_user = User(name=name)
        db.session.add(new_user)
        db.session.commit()
        return new_user

    def get_users(self):
        return User.query.all()

    def get_user(self, user_id):
        return User.query.get(user_id)

    def get_movies(self, user_id):
        return Movie.query.filter_by(user_id=user_id).all()

    def get_movie(self, movie_id):
        return Movie.query.get(movie_id)

    def add_movie(self, user_id, title, director=None, year=None, poster_url=None):
        new_movie = Movie(
            user_id=user_id,
            title=title,
            director=director,
            year=year,
            poster_url=poster_url
        )
        db.session.add(new_movie)
        db.session.commit()
        return new_movie

    def update_movie(self, movie_id, data):
        movie_to_update = Movie.query.get(movie_id)
        if movie_to_update is None:
            return None
        if 'title' in data:
            movie_to_update.title = data['title']
        if 'director' in data:
            movie_to_update.director = data['director']
        if 'year' in data:
            movie_to_update.year = data['year']
        if 'poster_url' in data:
            movie_to_update.poster_url = data['poster_url']
        db.session.commit()
        return movie_to_update

    def delete_movie(self, movie_id):
        movie_to_delete = Movie.query.get(movie_id)
        if movie_to_delete is not None:
            db.session.delete(movie_to_delete)
            db.session.commit()