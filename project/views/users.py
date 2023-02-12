import token

import jwt
import user_profile as user_profile
from flask import request
from flask_restx import Namespace, Resource
from requests import api

from project.constants import PWD_HASH_SALT
from project.dao.model.user import UserSchema
from project.implemented import user_service
from project.service.auth import AuthService
from project.setup_db import db
from project.utils import auth_required, login_required

user_ns = Namespace('user')

# @api.route('/', endpoint='profile_view')
# class UserProfileView(Resource):
#
#     @api.marshal_with(user_profile, code=200, description='OK')
#     @login_required
#     def get(self, user_id: int):
#         """
#         Получить профиль пользователя.
#         """
#         return AuthService(db.session).get_user_profile(user_id)


# @api.route('/', endpoint='profile_view')
# class UserProfileView(Resource):
#
#     @api.marshal_with(user_profile, code=200, description='OK')
#     @login_required
#     def get(self, user_id: int):
#         """
#         Получить профиль пользователя.
#         """
#         return AuthService(db.session).get_user_profile(user_id)
# @user_ns.route('/')
class UsersView(Resource):
    @login_required
    def get(self, user_id: int):
        """
        Получить профиль пользователя.
        """
        return AuthService(db.session).get_user_profile(user_id)



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