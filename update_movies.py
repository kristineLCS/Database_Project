from app import app, db
from database.database import Movie, fetch_movie_data

with app.app_context():
    movies = Movie.query.all()
    for movie in movies:
        movie_data = fetch_movie_data(movie.title)
        if movie_data:
            movie.actors = movie_data.get('actors', '')
            db.session.commit()
    print("Database updated with actors information.")


from app import app, db
from database.database import fetch_movie_data
from database.model import Movie

def update_genres_and_actors():
    """
    Fetches genres and actors for all movies in the database
    using the OMDB API and updates the records.
    """
    with app.app_context():
        movies = Movie.query.all()  # Get all movies from the database
        
        for movie in movies:
            print(f"Updating movie: {movie.title}")
            movie_data = fetch_movie_data(movie.title)  # Fetch movie data using OMDB API
            
            if movie_data:
                # Update genres and actors if the API returned them
                movie.genre = movie_data.get("genre", movie.genre)  # Keep existing if not fetched
                movie.actors = movie_data.get("actors", movie.actors)
                db.session.commit()  # Save changes
                print(f"Updated: {movie.title} (Genres: {movie.genre}, Actors: {movie.actors})")
            else:
                print(f"Could not fetch data for {movie.title}")
        
        print("Genres and actors update complete.")


if __name__ == "__main__":
    update_genres_and_actors()
