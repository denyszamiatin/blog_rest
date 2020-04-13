from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow.exceptions import ValidationError
from marshmallow import validates, fields
from . import models


class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = models.User
        exclude = "id",
        load_instance = True


class UserSchemaGet(SQLAlchemyAutoSchema):
    class Meta:
        model = models.User
        exclude = "id", "password",


class PostSchema(SQLAlchemyAutoSchema):
    author = fields.Nested(UserSchemaGet)

    class Meta:
        model = models.Post
        exclude = "id",
        load_instance = True

    @validates("title")
    def is_caps(self, value:str):
        if not value[0].isupper():
            raise ValidationError("First letter in the title must be in uppercase")
