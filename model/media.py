class Movie():
    def __init__(self, id, title, poster_path, overview, vote_average):
        self.id = id
        self.title = title
        self.poster_path = 'http://image.tmdb.org/t/p/w185' + poster_path
        self.overview = overview
        self.vote_average = vote_average
