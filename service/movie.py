from flask import current_app

from dao.model.movie import MovieSchema
from dao.movie import MovieDAO


class MovieService:
    def __init__(self, dao: MovieDAO):
        self.dao = dao

    def get_by_id(self, bid):
        movie = self.dao.get_by_id(bid)

        return MovieSchema().dump(movie)

    def get_all_movies(self, data):
        movie_query = self.dao.get_movies()

        status = data.get('status')
        page = data.get('page')

        if status and status == 'new':
            movie_query == self.dao.get_new(movie_query)

        if page:
            limit = current_app.config['ITEMS_PER_PAGE']
            offset = (page - 1) * limit
            movie_query = self.dao.get_pages(movie_query, limit, offset)

        movies = self.dao.get_all(movie_query)

        return MovieSchema(many=True).dump(movies)

