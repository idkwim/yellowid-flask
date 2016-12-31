from app import db
from .message import BaseMessage, HomeMessage, SuccessMessage, FailMessage
from .model import User
from .keyboard import Keyboard


class Singleton(type):
    instance = None

    def __call__(cls, *args, **kwargs):
        if not cls.instance:
            cls.instance = super(Singleton, cls).__call__(*args, **kwargs)
        return cls.instance


class APIManager(metaclass=Singleton):
    def process(self, mode, *args):
        options = {
            "home": self.return_home_keyboard,
            "message": self.handle_message,
            "add": self.add_friend,
            "block": self.block_friend,
            "exit": self.exit_chatroom,
            "fail": self.handle_fail,
        }
        return options.get(mode, self.handle_fail)(*args)

    def return_home_keyboard(self):
        message = MessageHandler.get_home_message()
        return message

    def handle_message(self, data):
        user_key = data["user_key"]
        request_type = data["type"]
        content = data["content"]

        message = MessageHandler.get_base_message()
        return message

    def add_friend(self, data):
        user_key = data["user_key"]
        message = MessageHandler.get_success_message()
        return message

    def block_friend(self, user_key):
        message = MessageHandler.get_success_message()
        return message

    def exit_chatroom(self, user_key):
        message = MessageHandler.get_success_message()
        return message

    def handle_fail(self):
        message = MessageHandler.get_fail_message()
        return message


class MessageManager(metaclass=Singleton):
    def get_base_message(self):
        base_message = BaseMessage().get_message()
        return base_message

    def get_home_message(self):
        home_message = HomeMessage().get_message()
        return home_message

    def get_fail_message(self):
        fail_message = FailMessage().get_message()
        return fail_message

    def get_success_message(self):
        success_message = SuccessMessage().get_message()
        return success_message


class DBManager(metaclass=Singleton):
    def query(self, model, **kwargs):
        return model.query.filter_by(**kwargs).first()

    def delete(self, obj):
        db.session.delete(obj)
        self.commit()

    def add(self, obj):
        db.session.add(obj)
        self.commit()

    def commit(self):
        db.session.commit()

APIHandler = APIManager()
MessageHandler = MessageManager()
DBHandler = DBManager()
