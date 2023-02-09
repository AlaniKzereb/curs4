import token

import jwt
from flask import request
from flask_restx import Resource, Namespace

from project.constants import PWD_HASH_SALT
from project.dao.model.user import UserSchema
from project.implemented import user_service
from project.utils import authorized, auth_required

user_ns = Namespace('user')


@user_ns.route('/')
class UsersView(Resource):
    @auth_required
    def get(self):
        user = user_service.get_one(uid)
        sm_d = UserSchema().dump(user)
        return sm_d, 200

    def patch(self, uid):
        user_service.patch(uid)
        return "ok", 204

    def put(self, uid):
        req_json = request.json
        if "id" not in req_json:
            req_json['id'] = uid
        user_service.update(req_json)
        return "ok", 204

    def post(self):
        req_json = request.json
        user = user_service.create(req_json)
        return "ok", 201, {"location":f"/users/{user.id}"}


@user_ns.route('/password')
class UserView(Resource):
    # @user_check
    def put(self, uid):
        req_json = request.json
        if "id" not in req_json:
            req_json['id'] = uid
        user_service.update(req_json)
        return "ok", 204