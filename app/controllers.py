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


api.add_resource(PostListApi, '/posts')
