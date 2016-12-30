from app import db
from .message import BaseMessage, HomeMessage, SuccessMessage, FailMessage
from .model import User


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
        userKey = data["user_key"]
        requestType = data["type"]
        content = data["content"]

        message = MessageHandler.get_base_message()
        return message

    def add_friend(self, data):
        userKey = data["user_key"]
        message = MessageHandler.get_success_message()
        return message

    def block_friend(self, userKey):
        message = MessageHandler.get_success_message()
        return message

    def exit_chatroom(self, userKey):
        message = MessageHandler.get_success_message()
        return message

    def handle_fail(self):
        message = MessageHandler.get_fail_message()
        return message


class MessageManager(metaclass=Singleton):
    def get_base_message(self):
        baseMessage = BaseMessage().get_message()
        return baseMessage

    def get_home_message(self):
        homeMessage = HomeMessage().get_message()
        return homeMessage

    def get_fail_message(self):
        failMessage = FailMessage().get_message()
        return failMessage

    def get_success_message(self):
        successMessage = SuccessMessage().get_message()
        return successMessage


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
