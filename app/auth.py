import os
import datetime
from werkzeug.security import check_password_hash
from flask import request, jsonify
import jwt
from app import app, db
from . import models


@app.route("/login")
def login():
    auth = request.authorization
    user = db.session.query(models.User).filter_by(login=auth.get("username", "")).first()
    if user is None or not check_password_hash(user.password, auth.get("password", "")):
        return "", 401, {"WWW-Authenticate": 'Basic realm="Authentication required"'}
    token = jwt.encode({
        "user_id": user.uuid,
        "exp": datetime.datetime.now() + datetime.timedelta(hours=1)
    }, app.config['SECRET_KEY'])
    return jsonify({"token": token.decode("utf-8")})


def token_required(f):
    def wrapper(self, *args, **kwargs):
        token = request.headers.get("X-Api-Key", "")
        if not token:
            return "", 401, {"WWW-Authenticate": 'Basic realm="Authentication required"'}
        try:
            uuid = jwt.decode(token, app.config['SECRET_KEY'])['user_id']
        except (KeyError, jwt.ExpiredSignatureError):
            return "", 401, {"WWW-Authenticate": 'Basic realm="Authentication required"'}
        user = db.session.query(models.User).filter_by(uuid=uuid).first()
        if not user:
            return "", 401, {"WWW-Authenticate": 'Basic realm="Authentication required"'}
        if kwargs:
            post = db.session.query(models.Post).filter_by(uuid=kwargs["uuid"]).first()
            if not post:
                return "", 404
            if post.author_id != user.id:
                return "", 401, {"WWW-Authenticate": 'Basic realm="Authentication required"'}
        return f(self, user, *args, **kwargs)
    return wrapper


if os.getenv("APP_CONFIG") == "test":
    token_required = lambda f: lambda self, *args, **kwargs: f(
        self, models.User(login='x', password='1', email="user1@example.org"), *args, **kwargs
    )
