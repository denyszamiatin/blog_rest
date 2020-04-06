from flask_restful import Resource, reqparse
from app import api, db
from . import models

parser = reqparse.RequestParser()
parser.add_argument("title")
parser.add_argument("body")
parser.add_argument("date")


class PostListApi(Resource):

    def post(self):
        args = parser.parse_args()
        post = models.Post(args["title"], args["body"], args["date"])
        db.session.add(post)
        db.session.commit()
        return post.to_json(), 201

    def get(self):
        posts = db.session.query(models.Post).all()
        return [post.to_json() for post in posts]


class PostApi(Resource):

    def get(self, uuid):
        post = db.session.query(models.Post).filter_by(uuid=uuid).first()
        if post is None:
            return "", 404
        return post.to_json()

    def put(self, uuid):
        args = parser.parse_args()
        post = db.session.query(models.Post).filter_by(uuid=uuid).first()
        if post is None:
            return "", 404
        post.title = args['title']
        post.body = args['body']
        post.pub_date = args['date']
        db.session.add(post)
        db.session.commit()
        return post.to_json()

    def delete(self, uuid):
        post = db.session.query(models.Post).filter_by(uuid=uuid).first()
        if post is None:
            return "", 404
        db.session.delete(post)
        db.session.commit()
        return "", 204



api.add_resource(PostListApi, '/posts')
api.add_resource(PostApi, '/posts/<uuid>')
