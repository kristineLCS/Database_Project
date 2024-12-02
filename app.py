from flask import Flask, jsonify, request, render_template, redirect, url_for, flash, session
import os
import requests
import random
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash
from database.database import db, populate_database
from database.model import User, UserMovie, Movie
from sqlalchemy import or_
from flask_login import current_user, login_required, LoginManager, login_user, logout_user

# Load environment variables
load_dotenv()

OMDB_API_KEY = os.getenv('OMDB_API_KEY')


# Initialize the Flask app
app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Bind SQLAlchemy to the app
db.init_app(app)

# Routes
@app.route('/')
def home():
    # Get all movies from the database
    movies = Movie.query.all()

    # Check if there are at least 8 movies; otherwise, just use all available
    if len(movies) > 8:
        # Select 8 random movies from the list
        random_movies = random.sample(movies, 8)
    else:
        # If less than 8 movies, show all available movies
        random_movies = movies

    # Define genres for grouping
    genres = ['romance', 'drama', 'action', 'comedy']

    # Create a dictionary to hold filtered movies by genre
    genre_movies = {}
    for genre in genres:
        genre_movies[genre] = [movie for movie in movies if genre.lower() in movie.genre.lower()]

    # Pass both random movies for the main slideshow and genre_movies for genre-specific slideshows
    return render_template('index.html', movies=random_movies, genre_movies=genre_movies)


@app.route('/admin_dashboard')
@login_required
def admin_dashboard():
    if not current_user.is_admin:  # Ensure only admins can access
        flash('Unauthorized access.', 'error')
        return redirect(url_for('user_profile'))
    return render_template('admin_dashboard.html')  # Your admin dashboard page


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password_hash, password):
            login_user(user)  # Logs the user in with Flask-Login

            # Set session variables to indicate user and admin status
            session['user_id'] = user.user_id

            # Debug print statement to check session data
            print("Session after login:", session)

            if user.is_admin:
                session['is_admin'] = True
                return redirect(url_for('admin_dashboard'))  # Redirect to admin dashboard
            else:
                session['is_admin'] = False
                return redirect(url_for('user_profile'))  # Redirect to user profile
        else:
            flash('Invalid username or password.', 'error')

    return render_template('login.html')



@app.route('/protected')
@login_required
def protected():
    return "This is a protected route."

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if User.query.filter_by(username=username).first():
            return "Username already exists", 409

        new_user = User(
            username=username,
            password_hash=generate_password_hash(password)
        )
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for('user_profile', user_id=new_user.user_id))

    return render_template('signup.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    session.clear()
    return redirect(url_for("home"))


@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        # Get the search query from the form data
        search_query = request.form.get('query', '').strip()
    else:
        # Get the search query from the URL parameters
        search_query = request.args.get("query", "").strip()

    query_type = request.args.get("type", "title")  # Default to title search

    # Perform the search based on the query type
    if query_type == "actor":
        results = Movie.query.filter(Movie.actors.ilike(f"%{search_query}%")).all()
    elif query_type == "genre":
        results = Movie.query.filter(Movie.genre.ilike(f"%{search_query}%")).all()
    elif query_type == "director":
        results = Movie.query.filter(Movie.director.ilike(f"%{search_query}%")).all()
    else:  # Default: Search by title or general query
        results = Movie.query.filter(
            or_(
                Movie.title.ilike(f"%{search_query}%"),
                Movie.actors.ilike(f"%{search_query}%"),
                Movie.genre.ilike(f"%{search_query}%"),
                Movie.director.ilike(f"%{search_query}%")
            )
        ).all()

    # Render the search results
    return render_template('search_result.html', results=results, query=search_query)



@app.route('/add_to_profile', methods=['POST'])
@login_required
def add_to_profile():
    movie_id = request.form.get('movie_id')
    movie = Movie.query.get(movie_id)

    if not movie:
        flash('Movie not found.', 'error')
        return redirect(url_for('search_results'))

    # Check if the movie is already in the user's profile using a query
    existing_entry = UserMovie.query.filter_by(user_id=current_user.user_id, movie_id=movie.movie_id).first()

    if not existing_entry:
        user_movie = UserMovie(user_id=current_user.user_id, movie_id=movie.movie_id)
        db.session.add(user_movie)
        db.session.commit()
        flash('Movie added to your profile!', 'success')
    else:
        flash('Movie is already in your profile.', 'info')

    return redirect(url_for('user_profile'))  # Redirect to user's profile page



@app.route('/update_watched_status', methods=['POST'])
@login_required
def update_watched_status():
    data = request.get_json()
    user_movie_id = data.get('user_movie_id')
    watched = data.get('watched')

    # Find the UserMovie entry and update the watched status
    user_movie = UserMovie.query.filter_by(id=user_movie_id, user_id=current_user.user_id).first()
    if user_movie:
        user_movie.watched = watched
        db.session.commit()
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'message': 'Movie not found or not authorized.'}), 404



@app.route('/delete_movie', methods=['POST'])
@login_required
def delete_movie():
    data = request.get_json()
    user_movie_id = data.get('user_movie_id')

    user_movie = UserMovie.query.get(user_movie_id)

    if user_movie and user_movie.user_id == current_user.user_id:
        db.session.delete(user_movie)
        db.session.commit()
        return jsonify({'success': True})
    else:
        return jsonify({'success': False}), 400



# Mark Movie as Watched/Unwatched
@app.route('/toggle_watched/<int:movie_id>', methods=['POST'])
@login_required
def toggle_watched(movie_id):
    entry = UserMovie.query.filter_by(user_id=current_user.user_id, movie_id=movie_id).first()
    if entry:
        entry.watched = not entry.watched
        db.session.commit()
        status = "watched" if entry.watched else "not watched"
        flash(f"Movie marked as {status}.", "success")
    else:
        flash("Movie not found in your list.", "error")
    return redirect(url_for('user_profile', user_id=current_user.user_id))



# In your user_profile route
@app.route('/user_profile')
@login_required
def user_profile():
    # Retrieve the user's movies with their watched status
    user_movies = UserMovie.query.filter_by(user_id=current_user.user_id).all()
    return render_template('user_profile.html', user_movies=user_movies)


@app.route('/movies', methods=['GET'])
def get_movies():
    movies = Movie.query.all()
    return jsonify([{
        "movie_id": movie.movie_id,
        "title": movie.title,
        "release_year": movie.release_year,
        "genre": movie.genre,
        "director": movie.director,
        "plot": movie.plot,
        "poster_url": movie.poster_url
    } for movie in movies])

@app.route('/genre/<genre_name>')
def show_genre(genre_name):
    # Query the database for movies of the specified genre
    movies = Movie.query.filter(Movie.genre.contains(genre_name)).all()

    return render_template('genre.html', genre=genre_name, movies=movies)


@app.route('/actor/<string:actor_name>')
def movies_by_actor(actor_name):
    movies = Movie.query.filter(Movie.actors.ilike(f'%{actor_name}%')).all()
    return render_template('actor_movies.html', actor=actor_name, movies=movies)

# @app.route('/movie/<int:movie_id>', methods=['GET'])
# def movie_details(movie_id):
#     movie = Movie.query.get_or_404(movie_id)
#     return render_template('movie_details.html', movie=movie)

@app.route('/fetch_movies', methods=['POST'])
def fetch_movies():
    movie_titles = request.json.get("titles", [])
    populate_database(movie_titles)
    return jsonify({"message": "Movies fetched and added to the database"}), 201

@app.route('/fetch_movie_from_omdb', methods=['POST'])
@login_required
def fetch_movie_from_omdb():
    if not current_user.is_admin:
        flash('Unauthorized access.', 'error')
        return redirect(url_for('user_profile'))

    movie_title = request.form.get('movie_title')
    response = requests.get(f"http://www.omdbapi.com/?t={movie_title}&apikey={OMDB_API_KEY}")
    movie_data = response.json()

    if movie_data['Response'] == 'True':
        # Render the movie details on a new page or redirect to admin_dashboard with the data
        return render_template('admin_dashboard.html', movie=movie_data)
    else:
        flash('Movie not found or error occurred while fetching from OMDb.', 'error')
        return redirect(url_for('admin_dashboard'))
    
@app.route('/add_movie_from_omdb', methods=['POST'])
@login_required
def add_movie_from_omdb():
    if not current_user.is_admin:
        flash('Unauthorized access.', 'error')
        return redirect(url_for('user_profile'))

    title = request.form.get('title')
    release_year = request.form.get('release_year')
    genre = request.form.get('genre')
    director = request.form.get('director')
    actors = request.form.get('actors')
    plot = request.form.get('plot')
    poster_url = request.form.get('poster_url')

    # Create a new Movie instance
    new_movie = Movie(
        title=title,
        release_year=release_year,
        genre=genre,
        director=director,
        actors=actors,
        plot=plot,
        poster_url=poster_url
    )

    db.session.add(new_movie)
    db.session.commit()
    flash('Movie added successfully!', 'success')
    return redirect(url_for('admin_dashboard'))



@app.errorhandler(404)
def page_not_found(e):
    return render_template('index.html'), 404

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Movie': Movie, 'User': User, 'populate_database': populate_database}

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("Database initialized.")

    app.run(debug=True, port=8080)
