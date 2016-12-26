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
    def process(self, mode, data=None):
        if mode is "home":
            message = MessageAdmin.get_home_message()
            return message
        elif mode is "message":
            user_key = data["user_key"]
            request_type = data["type"]
            content = data["content"]
            message = MessageAdmin.get_base_message()
            return message
        elif mode is "add":
            user_key = data["user_key"]
            message = MessageAdmin.get_success_message()
            return message
        elif mode is "block":
            user_key = data
            message = MessageAdmin.get_success_message()
            return message
        elif mode is "exit":
            user_key = data
            message = MessageAdmin.get_success_message()
            return message
        elif mode is "fail":
            message = MessageAdmin.get_fail_message()
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

APIAdmin = APIManager()
MessageAdmin = MessageManager()
DBAdmin = DBManager()
