from project.dao.model.movie import Movie


class MovieDAO:
    def __init__(self, session):
        self.session = session

    def get_by_id(self, bid):
        return self.session.query(Movie).filter(Movie.id == bid).one_or_none()

    def get_movies(self):
        return self.session.query(Movie)

    def get_all(self, query):
        return self.session.query(Movie).all()


    def get_new(self, query):
        return query.order_by(Movie.year.desc())

    def get_pages(self, query, limit, offset):
        return query.limit(limit).offset(offset)
