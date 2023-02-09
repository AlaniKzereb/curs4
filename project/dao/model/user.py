from marshmallow import Schema, fields

from project.dao.model.basemodel import BaseModelId
from project.setup_db import db


class User(BaseModelId, db.Model):
	__tablename__ = 'user'
	email = db.Column(db.String, unique=True)
	# email = db.Column(db.String, unique=True, Nullable=False)
	password = db.Column(db.String)
	name = db.Column(db.String)
	surname = db.Column(db.String)
	favorite_genre = db.Column(db.String)


class UserSchema(Schema):
	id = fields.Int(required=True)
	email = fields.Str(required=True)
	password = fields.Str(required=True)
	name = fields.Str()
	surname = fields.Str()
	favorite_genre = fields.Str()

