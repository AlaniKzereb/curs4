from flask_restx import Resource, Namespace

from project.dao.model.director import DirectorSchema
from project.implemented import director_service

director_ns = Namespace('directors')


@director_ns.route('/')
class DirectorsView(Resource):
    def get(self):
        rs = director_service.get_all()
        res = DirectorSchema(many=True).dump(rs)
        return res, 200


@director_ns.route('/<int:rid>')
class DirectorView(Resource):
    def get(self, rid):
        director = director_service.get_item_by_id(rid)
        return director, 200
