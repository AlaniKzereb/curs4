from functools import wraps

import jwt
from flask import request, jsonify
from flask_restx import abort

from constants import PWD_HASH_SALT

secret = 's3cR$eT'
algo = 'HS256'

def auth_required(func):
    def wrapper(*args, **kwargs):
        if 'Authorization' not in request.headers:
            abort(401)

        data = request.headers['Authorization']
        token = data.split("Bearer ")[-1]
        try:
            jwt.decode(token, PWD_HASH_SALT, algorithms=['HS256'])
        except Exception as e:
            print("JWT Decode Exception", e)
            abort(401)
        return func(*args, **kwargs)

    return wrapper


def admin_required(func):
    def wrapper(*args, **kwargs):
        if 'Authorization' not in request.headers:
            abort(401)

        data = request.headers['Authorization']
        token = data.split("Bearer ")[-1]
        try:
            user = jwt.decode(token, PWD_HASH_SALT, algorithms=['HS256'])
            role = user.get("role")
            if role != "admin":
                abort(400)
        except Exception as e:
            print("JWT Decode Exception", e)
            abort(401)
        return func(*args, **kwargs)

    return wrapper



#Попытки разобраться с декоратором для юзера
def user_check(func):
    def wrapper(*args, **kwargs):
        if 'Authorization' not in request.headers:
            abort(401)

        data = request.headers['Authorization']
        token = data.split("Bearer ")[-1]
        try:
            user = jwt.decode(token, PWD_HASH_SALT, algorithms=['HS256'])
            uid = user.get("id")
        except Exception as e:
            print("JWT Decode Exception", e)
            abort(401)
        return func(id, *args, **kwargs)
    return wrapper



def authorized(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'Authorization' not in request.headers:
            abort(401)

        data = request.headers['Authorization']
        token = data.split("Bearer ")[-1]
        try:
            user = jwt.decode(token, PWD_HASH_SALT, algorithms=['HS256'])
            user_id = user.get("id")
        except:
            return jsonify({"success": False}), 500
        return func(user_id, *args, **kwargs)
    return wrapper