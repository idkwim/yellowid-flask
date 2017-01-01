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


def test_fail_message(test_client):
    data = dict(
        user_key="test_id"
    )
    json_data = json.dumps(data)
    response = test_client.post("/message", data=json_data, content_type="application/json")
    assert response.status_code == 400
    message = json.loads(response.data)
    assert message["message"]["text"] == "오류가 발생하였습니다."


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


def test_remove_keyboard(test_client):
    msg = message.BaseMessage()
    msg.remove_keyboard()
    assert "keyboard" not in msg.get_message()


def test_add_photo(test_client):
    msg = message.BaseMessage()
    url = "https://www.python.org/static/img/python-logo.png"
    msg.add_photo(url, 320, 240)
    assert "photo" in msg.get_message()["message"]
    assert url == msg.get_message()["message"]["photo"]["url"]
    assert 320 == msg.get_message()["message"]["photo"]["width"]
    assert 240 == msg.get_message()["message"]["photo"]["height"]


def test_add_message_button(test_client):
    msg = message.BaseMessage()
    url = "https://www.ruby-lang.org/ko/"
    msg.add_message_button(url, "루비")
    assert "message_button" in msg.get_message()["message"]
    assert url == msg.get_message()["message"]["message_button"]["url"]
    assert "루비" == msg.get_message()["message"]["message_button"]["label"]


def test_update_message(teset_client):
    msg = message.BaseMessage()
    msg.update_message("파이썬")
    assert "파이썬" == msg.get_message()["message"]["text"]


def test_update_message(test_client):
    msg = message.BaseMessage()
    msg.update_keyboard(["파이썬", "루비", "아희"])
    assert ["파이썬", "루비", "아희"] == msg.get_message()["keyboard"]["buttons"]


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
