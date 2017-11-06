from flask import Flask, render_template
import requests

from model.media import Movie
from model.video import Video

app = Flask(__name__)

URL = 'https://api.themoviedb.org/'
PARAMS = {'api_key': '60dbe1af2d9d27a66e65f26e2ec0db7a', 'page': 1}

#list of movies cached in global variables to avoid reloading api
moviesTopRated = []
moviesPopular = []
moviesNowPlaying = []
moviesUpcoming = []

#movie id and video dictionary cache
trailerKeysDict = {}


@app.route('/')
@app.route('/home/')
def home():
    global moviesTopRated
    if len(moviesTopRated) == 0: #if list has no items cached, load movies
        moviesTopRated = getMovies('3/movie/top_rated/')
    return render_template('index.html', movies=moviesTopRated, pageHeading='Top Rated')


@app.route('/popular/')
def popular():
    global moviesPopular
    if len(moviesPopular) == 0: #if list has no items cached, load movies
        moviesPopular = getMovies('3/movie/popular/')
    return render_template('index.html', movies=moviesPopular, pageHeading='Popular')


@app.route('/now/')
def now_playing():
    global moviesNowPlaying
    if len(moviesNowPlaying) == 0: #if list has no items cached, load movies
        moviesNowPlaying = getMovies('3/movie/now_playing/')
    return render_template('index.html', movies=moviesNowPlaying, pageHeading='Now Playing')


@app.route('/upcoming/')
def upcoming():
    global moviesUpcoming
    if len(moviesUpcoming) == 0: #if list has no items cached, load movies
        moviesUpcoming = getMovies('3/movie/upcoming/')
    return render_template('index.html', movies=moviesUpcoming, pageHeading='Upcoming')


@app.route('/trailer/<id>')
def loadTrailer(id):
    global trailerKeysDict
    if (id not in trailerKeysDict): #if dict does not have this id as key, load data
        tRequest = requests.get(url=URL + '3/movie/' + str(id) + '/videos', params=PARAMS)
        data = tRequest.json()['results']
        for item in data:
            if (item['site'] == 'YouTube'): #make sute its a youtube result
                trailerKeysDict[id] = Video(item['id'], item['key'], item['name'], item['site'], item['type']) #add Video item in dictionary with respective id as key
                return render_template('trailer.html', video=trailerKeysDict[id])
    return '<h2>Oops, No trailer found!</h2>' #if api returned empty results


def getMovies(route):
    request = requests.get(url=URL + route, params=PARAMS)
    data = request.json()['results']
    movies = [] #list of movies to be returned
    for item in data:
        movies.append(Movie(item['id'], item['title'], item['poster_path'], item['overview'], item['vote_average'])) #add movie item to list
    return movies


if __name__ == '__main__':
    app.run(debug=True)
