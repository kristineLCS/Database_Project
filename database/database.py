import os
import requests
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy

# Load environment variables
load_dotenv()
OMDB_API_KEY = os.getenv('OMDB_API_KEY')
if not OMDB_API_KEY:
    raise Exception("OMDB_API_KEY not found in environment variables.")

# Initialize SQLAlchemy instance
db = SQLAlchemy()

# Fetch movie data from OMDB API
def fetch_movie_data(title):
    """Fetch movie data from the OMDB API using a movie title."""
    url = f"http://www.omdbapi.com/?t={title}&apikey={OMDB_API_KEY}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if data.get("Response") == "True":
            return {
                "title": data.get("Title"),
                "release_year": int(data.get("Year", 0)),
                "genre": data.get("Genre", ""),
                "actors": data.get("Actors", ""),
                "director": data.get("Director"),
                "plot": data.get("Plot"),
                "poster_url": data.get("Poster")
            }
    return None

# Add or update a movie in the database
def add_or_update_movie(movie_data):
    from database.model import Movie  # Import here to prevent circular import
    existing_movie = Movie.query.filter_by(title=movie_data["title"]).first()
    if existing_movie:
        # Update existing movie details
        existing_movie.release_year = movie_data["release_year"]
        existing_movie.genre = movie_data["genre"]
        existing_movie.director = movie_data["director"]
        existing_movie.plot = movie_data["plot"]
        existing_movie.poster_url = movie_data["poster_url"]
        print(f"Updated: {movie_data['title']}")
    else:
        # Add new movie
        new_movie = Movie(**movie_data)
        db.session.add(new_movie)
        print(f"Added: {movie_data['title']}")



# Add fetched movie to the database
def add_movie_to_db(movie_data):
    from database.model import Movie
    movie = Movie(
        title=movie_data.get("title"),
        release_year=movie_data.get("release_year", 0),
        genre=movie_data.get("genre"),  # Store the genre as a string (comma-separated)
        actors=movie_data.get("actors"),  # Store the actors as a string (comma-separated)
        director=movie_data.get("director"),
        plot=movie_data.get("plot"),
        poster_url=movie_data.get("poster_url")
    )
    db.session.add(movie)
    db.session.commit()


# Fetch and store a list of movies
def populate_database(movie_titles):
    """Fetch movie data for a list of titles and store them in the database."""
    for title in movie_titles:
        print(f"Fetching data for: {title}")
        movie_data = fetch_movie_data(title)
        if movie_data:
            add_or_update_movie(movie_data)
        else:
            print(f"Failed to fetch data for: {title}")
    db.session.commit()
    print("Database population complete.")

# Main script entry point
if __name__ == "__main__":
    # List of movies to add
    movie_list = [
        "The Shawshank Redemption",
        "The Godfather",
        "The Dark Knight",
        "Inception",
        "Fight Club",
        # Add more movie titles here
    ]

    # Import and use Flask app context
    from app import app
    with app.app_context():
        populate_database(movie_list)
