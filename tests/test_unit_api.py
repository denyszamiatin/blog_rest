from unittest import mock
from app import app


def test_post_create():
    with app.app_context():
        with mock.patch("app.db.session.add") as add, \
                mock.patch("app.db.session.commit") as commit:
            r = app.test_client().post("/posts", data={
                "title": "Title1",
                "body": "qwdfwbeeta",
                "date": "01.01.2020"
            })
            add.assert_called_once()
            commit.assert_called_once()
    assert r.status_code == 201
    assert r.json['title'] == "Title1"
