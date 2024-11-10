from flask_sqlalchemy import SQLAlchemy
from app import db  
import requests

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(100), unique=True)
    password_hash = db.Column(db.String(255))

class Movie(db.Model):
    __tablename__ = 'movies'

    movie_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    release_year = db.Column(db.Integer)
    genre = db.Column(db.String(100))
    director = db.Column(db.String(100))
    plot = db.Column(db.Text)
    poster_url = db.Column(db.String(255))

def fetch_movie_data(title):
    api_key = "da7690da"
    url = f"http://www.omdbapi.com/?t={title}&apikey={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None


def add_movie_to_db(movie_data):
    movie = Movie(
        title=movie_data.get("Title"),
        release_year=int(movie_data.get("Year", 0)),
        genre=movie_data.get("Genre"),
        director=movie_data.get("Director"),
        plot=movie_data.get("Plot"),
        poster_url=movie_data.get("Poster")
    )
    db.session.add(movie)
    db.session.commit()

def fetch_and_store_movies(movie_titles):
    for title in movie_titles:
        movie_data = fetch_movie_data(title)
        if movie_data and movie_data.get("Response") == "True":
            add_movie_to_db(movie_data)
            print(f"Added movie: {title}")
        else:
            print(f"Movie not found: {title}")

class Genre(db.Model):
    __tablename__ = 'genres'
    genre_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)