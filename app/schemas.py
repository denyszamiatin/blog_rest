from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow.exceptions import ValidationError
from marshmallow import validates
from . import models


class PostSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = models.Post
        exclude = "id",
        load_instance = True

    @validates("title")
    def is_caps(self, value:str):
        if not value[0].isupper():
            raise ValidationError("First letter in the title must be in uppercase")


