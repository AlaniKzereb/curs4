from marshmallow import Schema, fields

from project.dao.model.basemodel import BaseModelId
from project.setup_db import db


class Genre(BaseModelId, db.Model):
    __tablename__ = 'genre'
    name = db.Column(db.String)


class GenreSchema(Schema):
    id = fields.Int(required=True)
    name = fields.Str(required=True)
