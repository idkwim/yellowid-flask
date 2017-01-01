import pytest
from .config import *


@pytest.fixture
def app():
    main.app.config["TESTING"] = True
    main.app.config["SQLALCHEMY_DATABASE_URI"] = TEST_DATABASE_URI
    main.db.create_all()
    return main.app


@pytest.fixture
def test_client(app):
    return app.test_client()


def test_hello(test_client):
    assert isinstance(test_client, FlaskClient)


def test_keyboard(test_client):
    response = test_client.get("/keyboard")
    check_response(response)

    keyboard = json.loads(response.data)
    assert keyboard["type"] == "buttons"
    assert keyboard["buttons"] == ["홈버튼 1", "홈버튼 2", "홈버튼 3"]


def test_message(test_client):
    data = dict(
        user_key="test_id",
        type="text",
        content="홈버튼 1"
    )
    json_data = json.dumps(data)
    response = test_client.post("/message", data=json_data, content_type="application/json")
    check_response(response)

    message = json.loads(response.data)
    assert message["message"]["text"] == "기본 메시지"
    assert message["keyboard"]["type"] == "buttons"
    assert message["keyboard"]["buttons"] == ["홈버튼 1", "홈버튼 2", "홈버튼 3"]


def test_add_friend(test_client):
    data = dict(
        user_key="test_id"
    )
    json_data = json.dumps(data)
    response = test_client.post("/friend", data=json_data, content_type="application/json")
    check_success_response(response)


def test_block_firend(test_client):
    user_key = "test_id"
    response = test_client.delete("/friend/{}".format(user_key))
    check_success_response(response)


def test_exit_chatroom(test_client):
    user_key = "test_id"
    response = test_client.delete("/chat_room/{}".format(user_key))
    check_success_response(response)


def check_success_response(response):
    check_response(response)
    message = json.loads(response.data)
    assert message["message"] == "SUCCESS"
    assert message["comment"] == "정상 응답"


def check_response(response):
    assert response.status_code == 200
    assert response.content_type == "application/json"
    assert isinstance(response.data, bytes)
    assert isinstance(json.loads(response.data), dict)
