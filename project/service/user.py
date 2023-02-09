import calendar
import datetime
import hashlib

import jwt

from project.constants import PWD_HASH_SALT, PWD_HASH_ITERATIONS
from project.dao.user import UserDAO


class UserService:
    def __init__(self, dao: UserDAO):
        self.dao = dao

    def get_one(self, uid):
        return self.dao.get_one(uid)

    def get_all(self):
        return self.dao.get_all()

    def create(self, user_d):
        user_d['password'] = self.get_hash(user_d['password'])
        return self.dao.create(user_d)

    def update(self, user_d):
        self.dao.update(user_d)
        return self.dao

    def delete(self, uid):
        self.dao.delete(uid)

    def patch(self, user_d: str):
        user = self.get_one(user_d["id"])
        if "name" in user_d:
            user.title = user_d.get("name")
        if "surname" in user_d:
            user.description = user_d.get("surname")
        if "favorite_genre" in user_d:
            user.description = user_d.get("favorite_genre")

        self.dao.update(user)

    def get_hash(self, password):
        return hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),  # Convert the password to bytes
            PWD_HASH_SALT,
            PWD_HASH_ITERATIONS
        ).decode("utf-8", "ignore")

    def get_access_token(self, data: dict):

        min10 = datetime.datetime.utcnow() + datetime.timedelta(minutes=10)
        data['exp'] = calendar.timegm(min10.timetuple())
        access_token = jwt.encode(data, PWD_HASH_SALT)

        days130 = datetime.datetime.utcnow() + datetime.timedelta(days=130)
        data['exp'] = calendar.timegm(days130.timetuple())
        refresh_token = jwt.encode(data, PWD_HASH_SALT)

        return {'access_token': access_token, 'refresh_token': refresh_token, 'exp': data['exp']}

    def auth_user(self, email, password):
        user = self.dao.get_user_by_email(email)

        if not user:
            return None

        hash_password = self.get_hash(password)

        if hash_password != user.password:
            return None

        data = {
            'email': user.email,
        }

        return self.get_access_token(data)

    def check_refresh_token(self, refresh_token: str):
        try:
            data = jwt.decode(jwt=refresh_token, key=PWD_HASH_SALT, algorithms='HS256')
        except Exception as e:
            return None

        return self.get_access_token(data)
