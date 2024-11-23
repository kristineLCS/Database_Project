from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String
from sqlalchemy.orm import mapped_column
import requests
from database.database import db


class User(db.Model):
    __tablename__ = 'users'

    user_id = db.mapped_column(db.Integer, primary_key=True)
    username = db.mapped_column(db.String(50), unique=True)
    email = db.mapped_column(db.String(100), unique=True)
    password_hash = db.mapped_column(db.String(255))

class Movie(db.Model):
    __tablename__ = 'movies'

    movie_id = db.mapped_column(db.Integer, primary_key=True)
    title = db.mapped_column(db.String(100))
    release_year = db.mapped_column(db.Integer)
    genre = db.mapped_column(db.String(100))
    director = db.mapped_column(db.String(100))
    plot = db.mapped_column(db.Text)
    poster_url = db.mapped_column(db.String(255))

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
    genre_id = db.mapped_column(db.Integer, primary_key=True)
    name = db.mapped_column(db.String(50), unique=True)