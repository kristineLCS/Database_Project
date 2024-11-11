from flask import Flask, jsonify, request, render_template
import os
from database import db
from model import User, Movie, fetch_and_store_movies

app = Flask(__name__, static_folder='static')
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'not-set')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database with the app
db.init_app(app)

# Home Page
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/user/<int:user_id>')
def user_profile(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('user_profile.html', user=user)

@app.route('/marathon/<int:marathon_id>')
def marathon_details(marathon_id):
    # Fetch marathon details from the database
    marathon = Movie.query.get_or_404(marathon_id)
    return render_template('marathon_details.html', marathon=marathon)

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        search_query = request.form.get('query')
        # Perform search in the database, e.g., find marathons matching the query
        search_results = Movie.query.filter(Movie.title.contains(search_query)).all()
        return render_template('search_result.html', results=search_results, query=search_query)
    return render_template('search_result.html', results=[], query="")

@app.route('/fetch_movies', methods=['POST'])
def fetch_movies():
    movie_titles = request.json.get("titles", [])
    fetch_and_store_movies(movie_titles)
    return jsonify({"message": "Movies fetched and added to the database"}), 201

@app.route('/movies', methods=['GET'])
def get_movies():
    movies = Movie.query.all()
    movies_list = [{"title": movie.title, "release_year": movie.release_year} for movie in movies]
    return jsonify(movies_list)


@app.route('/movie', methods=['POST'])
def add_movie():
    data = request.get_json()
    new_movie = Movie(
        title=data['title'],
        release_year=data['release_year'],
        plot=data['plot'],
        poster_url=data['poster_url']
    )

    db.session.add(new_movie)
    db.session.commit()
    return jsonify({"message": "Movie added!"}), 201

@app.route('/movie/<int:movie_id>', methods=['PUT'])
def update(movie_id):
    data = request.get_json()
    movie = Movie.query.get_or_404(movie_id)
    movie.title = data['title']
    movie.release_year = data['release_year']
    movie.plot = data['plot']
    movie.poster_url = data['poster_url']

    db.session.commit()
    return jsonify({"message": "Movie updated!"})

@app.route('/movie/<int:movie_id>', methods=['DELETE'])
def delete_movie(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    db.session.delete(movie)
    db.session.commit()
    return jsonify({"message": "Movie removed!"})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=8080)
