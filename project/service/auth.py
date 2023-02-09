import calendar
import datetime
import hashlib

import jwt

from project.constants import PWD_HASH_SALT, PWD_HASH_ITERATIONS
from project.dao.user import UserDAO


class AuthService:
    def __init__(self, dao: UserDAO):
        self.dao = dao


    def auth_user(self, email, password):
        user = self.dao.get_user_by_email(email)

        if not user:
            return None

        hash_password = self.get_hash(password)

        if hash_password != user.password:
            return None

        data = {
            'email': user.email
        }

        return self.get_access_token(data)

    def get_hash(self, password: str):
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

    def check_refresh_token(self, refresh_token: str):
        try:
            data = jwt.decode(jwt=refresh_token, key=PWD_HASH_SALT, algorithms='HS256')
        except Exception as e:
            return None

        return self.get_access_token(data)
