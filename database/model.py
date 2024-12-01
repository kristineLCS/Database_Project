from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database.database import db
from flask_login import UserMixin


# Association table for User and Movie
user_movie = db.Table(
    'user_movie',
    db.Column('user_id', db.Integer, db.ForeignKey('users.user_id'), primary_key=True),
    db.Column('movie_id', db.Integer, db.ForeignKey('movies.movie_id'), primary_key=True)
)

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    # Relationships
    movies = db.relationship('Movie', secondary=user_movie, back_populates='users')
    user_movies = db.relationship('UserMovie', back_populates='user')


    # Override get_id() to return the user_id as a string
    def get_id(self):
        return str(self.user_id)  # Ensure that this returns a string


class UserMovie(db.Model):
    __tablename__ = 'user_movies'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.movie_id'), nullable=False)
    watched = db.Column(db.Boolean, default=False)

    # Relationships
    user = db.relationship('User', back_populates='user_movies')
    movie = db.relationship('Movie', back_populates='user_movies')


class Movie(db.Model):
    __tablename__ = 'movies'

    movie_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=True, nullable=False)
    release_year = db.Column(db.Integer, nullable=True)
    genre = db.Column(db.String(100), nullable=True)
    actors = db.Column(db.String(255))
    director = db.Column(db.String(100), nullable=True)
    plot = db.Column(db.Text, nullable=True)
    poster_url = db.Column(db.String(255), nullable=True)

    # Direct relationship with users
    users = db.relationship('User', secondary=user_movie, back_populates='movies')
    user_movies = db.relationship('UserMovie', back_populates='movie')

    def __repr__(self):
        return f'<Movie {self.title}>'



class MarathonMovie(db.Model):
    __tablename__ = 'marathon_movie'

    id = db.Column(db.Integer, primary_key=True)
    list_id = db.Column(db.Integer, db.ForeignKey('marathon_list.id'), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.movie_id'), nullable=False)

class Genre(db.Model):
    __tablename__ = 'genres'
    genre_id = db.mapped_column(db.Integer, primary_key=True)
    name = db.mapped_column(db.String(50), unique=True)