import json
import pytest
from app import app, db

@pytest.fixture
def etalon():
    return {
        "title": "Title1",
        "body": "qwdfwbeeta",
        "date": "2020-01-01T00:00:00",
    }


@pytest.fixture
def get_db():
    db.create_all()
    yield None
    db.drop_all()


@pytest.fixture
def post(get_db, etalon):
    r = app.test_client().post("/posts", data=json.dumps(etalon), content_type="application/json")
    return r.json['uuid']


def test_post_create(get_db, etalon):
    r = app.test_client().post("/posts", data=json.dumps(etalon), content_type="application/json")
    assert r.status_code == 201


def test_post_read(post, etalon):
    r = app.test_client().get(f"/posts/{post}")
    assert r.status_code == 200
    etalon['uuid'] = post
    assert r.json == etalon


def test_post_read_all(post):
    r = app.test_client().get("/posts")
    assert r.status_code == 200
    assert len(r.json) == 1


def test_post_update(post, etalon):
    etalon['title'] = "Title2"
    r = app.test_client().put(f"/posts/{post}", data=json.dumps(etalon), content_type="application/json")
    assert r.status_code == 200
    etalon['uuid'] = post
    assert r.json == etalon


def test_post_delete(post):
    r = app.test_client().delete(f"/posts/{post}")
    assert r.status_code == 204
    r = app.test_client().get(f"/post/{post}")
    assert r.status_code == 404
