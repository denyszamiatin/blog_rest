from flask import request, render_template
from flask_restful import Resource
from marshmallow.exceptions import ValidationError
from sqlalchemy.exc import IntegrityError
from . import api, db, app
from . import models
from . import schemas
from . import auth
from . import tasks


post_schema = schemas.PostSchema()
user_schema = schemas.UserSchema()
user_schema_get = schemas.UserSchemaGet()


class PostListApi(Resource):

    @auth.token_required
    def post(self, user):
        try:
            post = post_schema.load(request.json, session=db.session)
        except ValidationError as e:
            return {"message": str(e)}, 400
        post.author = user
        db.session.add(post)
        db.session.commit()
        emails = [user[0] for user in db.session.query(models.User.email).all()]
        subj = f"New post from {user.login}"
        message = render_template("email.txt", uuid=post.uuid)
        tasks.send_emails.delay('user1@example.org', emails, subj, message)
        return post_schema.dump(post), 201

    def get(self):
        posts = models.Post.query.paginate(
            int(request.args['p']),
            app.config['ITEMS_ON_PAGE'],
            False
        ).items
        return post_schema.dump(posts, many=True)


class PostApi(Resource):

    def get(self, uuid):
        post = db.session.query(models.Post).filter_by(uuid=uuid).first()
        if post is None:
            return "", 404
        return post_schema.dump(post)

    @auth.token_required
    def put(self, user, uuid):
        post = db.session.query(models.Post).filter_by(uuid=uuid).first()
        if post is None:
            return "", 404
        post = post_schema.load(request.json, instance=post, session=db.session)
        db.session.add(post)
        db.session.commit()
        return post_schema.dump(post)

    @auth.token_required
    def delete(self, user, uuid):
        post = db.session.query(models.Post).filter_by(uuid=uuid).first()
        if post is None:
            return "", 404
        db.session.delete(post)
        db.session.commit()
        return "", 204


class UserListApi(Resource):

    def post(self):
        try:
            user = user_schema.load(request.json, session=db.session)
        except ValidationError as e:
            return {"message": str(e)}, 400
        try:
            db.session.add(user)
            db.session.commit()
        except IntegrityError:
            return {"message": "User exists"}, 409
        return user_schema.dump(user), 201

    def get(self):
        users = db.session.query(models.User).all()
        return user_schema_get.dump(users, many=True)


api.add_resource(PostListApi, '/posts')
api.add_resource(PostApi, '/posts/<uuid>')
api.add_resource(UserListApi, '/users')
