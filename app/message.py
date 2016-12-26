from .keyboard import Keyboard


class Message:
    """
    반환될 메시지들의 추상 클래스입니다.
    별도의 수정은 필요하지 않습니다.
    본 클래스에 포함되어 있는 dict타입의 변수들은 조합을 위한 조각과 틀입니다.

    :param dict baseKeyboard: 키보드
    :param dict baseMessage: 키보드를 포함한 기본 메시지
    :param dict baseMessageButton: 메시지에 덧붙여질 메시지버튼
    """
    baseKeyboard = {
        "type": "buttons",
        "buttons": Keyboard.homeButtons,
    }

    baseMessage = {
        "message": {
            "text": "기본 메시지",
        },
        "keyboard": baseKeyboard,
    }

    baseMessageButton = {
        "message_button": {
            "label": "버튼에 들어갈 메시지",
            "url": "https://www.python.org",
        },
    }

    def __init__(self):
        self.returnedMessage = None

    def get_message(self):
        """
        인스턴스 변수인 returnedMessage를 반환합니다.
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
        return self.returnedMessage


class BaseMessage(Message):
    def __init__(self):
        super().__init__()
        self.returnedMessage = Message.baseMessage

    def convert_to_message_button(self, label, url):
        """
        반환될 메시지에 메시지버튼을 추가합니다.

        :param str label: 메시지버튼에 안내되는 메시지
        :param str url: 메시지버튼을 누르면 이동할 URL

        예제:
            다음과 같이 사용하세요:
            >>> a = BaseMessage()
            >>> a.convert_to_message_button("파이썬", "https://www.python.org")
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
        messageButton = Message.baseMessageButton
        messageButton["label"] = label
        messageButton["url"] = url
        self.returnedMessage["message"].update(messageButton)

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
        self.returnedMessage["message"]["text"] = message

    def update_keyboard(self, keyboard):
        """
        반환될 메시지의 키보드를 업데이트합니다.
        기본 동작은 덮어쓰기입니다.

        :param str keyboard: 반환될 메시지의 키보드

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
        _keyboard = Message.baseKeyboard
        _keyboard["buttons"] = keyboard
        self.returnedMessage["keyboard"] = _keyboard


class HomeMessage(Message):
    def __init__(self):
        super().__init__()
        self.returnedMessage = Message.baseKeyboard
        homeKeyboard = Keyboard.homeButtons
        self.returnedMessage["buttons"] = homeKeyboard


class FailMessage(BaseMessage):
    def __init__(self):
        super().__init__()
        self.updateMessage("오류가 발생하였습니다.")
        self.updateKeyboard(Keyboard.homeButtons)


class SuccessMessage(Message):
    def __init__(self):
        super().__init__()
        self.returnedMessage = "SUCCESS"
