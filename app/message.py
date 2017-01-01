from .keyboard import Keyboard
from ujson import dumps, loads


class classproperty(object):
    def __init__(self, getter):
        self.getter = getter

    def __get__(self, instance, owner):
        return self.getter(owner)


class Message:
    """
    반환될 메시지들의 추상 클래스입니다.
    별도의 수정은 필요하지 않습니다.
    본 클래스에 포함되어 있는 dict타입의 변수들은 조합을 위한 조각과 틀입니다.

    :param dict base_keyboard: 키보드
    :param dict base_message: 키보드를 포함한 기본 메시지
    :param dict base_message_button: 메시지에 덧붙여질 메시지버튼
    """
    _base_keyboard = {
        "type": "buttons",
        "buttons": Keyboard.home_buttons,
    }
    _base_message = {
        "message": {
            "text": "기본 메시지",
        },
        "keyboard": _base_keyboard,
    }
    _base_message_button = {
        "message_button": {
            "label": "버튼에 들어갈 메시지",
            "url": "https://www.python.org",
        },
    }
    _base_photo = {
        "photo": {
            "url": "https://www.python.org/static/img/python-logo.png",
            "width": 640,
            "height": 480,
        },
    }

    def __init__(self):
        self.returned_message = None

    @classproperty
    def base_keyboard(cls):
        return loads(dumps(cls._base_keyboard))

    @classproperty
    def base_message(cls):
        return loads(dumps(cls._base_message))

    @classproperty
    def base_message_button(cls):
        return loads(dumps(cls._base_message_button))

    @classproperty
    def base_photo(cls):
        return loads(dumps(cls._base_photo))

    def get_message(self):
        """
        인스턴스 변수인 returned_message 반환합니다.
        예제:
            다음과 같이 사용하세요:
            >>> a = BaseMessage()
            >>> a.get_message()
            {
                "message": {
                    "text": "기본 메시지"
                },
                "keyboard": {
                    "type": "buttons",
                    "buttons": [
                        "홈버튼 1",
                        "홈버튼 2",
                        "홈버튼 3"
                    ]
                }
            }

        :returns dict: 반환될 메시지
        """
        return self.returned_message


class BaseMessage(Message):
    """
    커스텀 메시지를 구현할 수 있는 클래스입니다.
    BaseMessage만 활용해도 되고 FailMessage처럼 상속받아 활용할 수도 있습니다.
    """
    def __init__(self):
        super().__init__()
        self.returned_message = Message.base_message

    def remove_keyboard(self):
        """
        반환될 메시지에서 키보드를 삭제합니다.

        예제:
            다음과 같이 사용하세요:
            >>> a = BaseMessage()
            >>> a.remove_keyboard()
            >>> a.get_message()
            {
                "message": {
                    "text": "기본 메시지"
                }
            }
        """
        if "keyboard" in self.returned_message:
            del self.returned_message["keyboard"]

    def add_photo(self, url, width, height):
        """
        반환될 메시지에 사진을 추가합니다.

        :param str url: 사진이 위치해 있는 URL
        :param int width: 사진의 가로 길이
        :param int height: 사진의 세로 길이

        예제:
            다음과 같이 사용하세요:
            >>> a = BaseMessage()
            >>> url = "https://www.python.org/static/img/python-logo.png"
            >>> a.add_photo(url, 400, 400)
            >>> a.get_message()
            {
                "message": {
                    "text": "기본 메시지",
                    "photo": {
                        "url": "https://www.python.org/static/img/python-logo.png",
                        "width": 400,
                        "height": 400,
                    }
                },
                "keyboard": 생략
            }
        """
        photo_message = Message.base_photo
        photo_message["url"] = url
        photo_message["width"] = width
        photo_message["height"] = height
        self.returned_message["message"].update(photo_message)

    def add_message_button(self, url, label):
        """
        반환될 메시지에 메시지버튼을 추가합니다.

        :param str url: 메시지버튼을 누르면 이동할 URL
        :param str label: 메시지버튼에 안내되는 메시지

        예제:
            다음과 같이 사용하세요:
            >>> a = BaseMessage()
            >>> a.add_message_button("https://www.python.org", "파이썬")
            >>> a.get_message()
            {
                "message": {
                    "text": "기본 메시지",
                    "message_button": {
                        "label": "파이썬",
                        "url": "https://www.python.org"
                    }
                },
                "keyboard": 생략
            }
        """
        button_message = Message.base_message_button
        button_message["label"] = label
        button_message["url"] = url
        self.returned_message["message"].update(button_message)

    def update_message(self, message):
        """
        반환될 메시지를 업데이트합니다.
        기본 동작은 덮어쓰기입니다.

        :param str message: 반환될 메시지

        예제:
            다음과 같이 사용하세요:
            >>> a = BaseMessage()
            >>> a.update_message("파이썬")
            >>> a.get_message()
            {
                "message": {
                    "text": "파이썬"
                },
                "keyboard": 생략
            }
        """
        self.returned_message["message"]["text"] = message

    def update_keyboard(self, keyboard):
        """
        반환될 메시지의 키보드를 업데이트합니다.
        기본 동작은 덮어쓰기입니다.

        :param list keyboard: 반환될 메시지의 키보드

        예제:
            다음과 같이 사용하세요:
            >>> a = BaseMessage()
            >>> a.update_keyboard(["파이썬", "루비", "아희"])
            >>> a.get_message()
            {
                "message": {
                    "text": "기본 메시지"
                },
                "keyboard": [
                    "파이썬",
                    "루비",
                    "아희"
                ]
            }
        """
        _keyboard = Message.base_keyboard
        _keyboard["buttons"] = keyboard
        self.returned_message["keyboard"] = _keyboard


class FailMessage(BaseMessage):
    """
    처리 중 예외가 발생했을 때 반환되는 메시지입니다.
    오류 메시지는 수정 가능하며 별도의 처리 로직을 추가하실 수 있습니다.
    """
    def __init__(self):
        super().__init__()
        self.update_message("오류가 발생하였습니다.")
        self.update_keyboard(Keyboard.home_buttons)


class HomeMessage(Message):
    """
    홈 메시지는 별도의 메시지가 없기에 Message를 상속받아 사용합니다.
    """
    def __init__(self):
        super().__init__()
        self.returned_message = Message.base_keyboard
        home_keyboard = Keyboard.home_buttons
        self.returned_message["buttons"] = home_keyboard


class SuccessMessage(Message):
    """
    친구 추가, 차단, 채팅방 나가기가 발생했을 때 성공적으로 처리되면 반환되는 메시지입니다.
    """
    def __init__(self):
        super().__init__()
        self.returned_message = "SUCCESS"
