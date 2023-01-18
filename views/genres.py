from flask_restx import Resource, Namespace

from implemented import genre_service

genre_ns = Namespace('genres')


@genre_ns.route('/')
class GenresView(Resource):
    def get(self):
        genre = genre_service.get_all()
        # res = GenreSchema(many=True).dump(rs)
        return genre, 200


@genre_ns.route('/<int:rid>')
class GenreView(Resource):
    def get(self, rid):
        genre = genre_service.get_item_by_id(rid)
        return genre, 200
