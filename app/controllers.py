from flask import request
from flask_restful import Resource
from marshmallow.exceptions import ValidationError
from app import api, db
from . import models
from . import schemas


post_schema = schemas.PostSchema()
posts_schema = schemas.PostSchema(many=True)


class PostListApi(Resource):

    def post(self):
        try:
            post = post_schema.load(request.json, session=db.session)
        except ValidationError as e:
            return {"message": str(e)}, 400
        db.session.add(post)
        db.session.commit()
        return post_schema.dump(post), 201

    def get(self):
        posts = db.session.query(models.Post).all()
        return posts_schema.dump(posts)


class PostApi(Resource):

    def get(self, uuid):
        post = db.session.query(models.Post).filter_by(uuid=uuid).first()
        if post is None:
            return "", 404
        return post_schema.dump(post)

    def put(self, uuid):
        post = db.session.query(models.Post).filter_by(uuid=uuid).first()
        if post is None:
            return "", 404
        try:
            post = post_schema.load(request.json, instance=post, session=db.session)
        except ValidationError as e:
            return {"message": str(e)}
        db.session.add(post)
        db.session.commit()
        return post_schema.dump(post)

    def delete(self, uuid):
        post = db.session.query(models.Post).filter_by(uuid=uuid).first()
        if post is None:
            return "", 404
        db.session.delete(post)
        db.session.commit()
        return "", 204


api.add_resource(PostListApi, '/posts')
api.add_resource(PostApi, '/posts/<uuid>')
