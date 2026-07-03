from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80))

    movies = db.relationship('Movie', backref='user', cascade='all, delete-orphan')

    def __repr__(self):
        return '<User %r>' % self.name

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(80))
    director = db.Column(db.String(80))
    year = db.Column(db.Integer)
    poster_url = db.Column(db.String(255))

    def __repr__(self):
        return '<Movie %r>' % self.title