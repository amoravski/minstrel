from pymongo import MongoClient
from mongoengine import *

class UserModel(Document):
    __tablename__ = 'users'

    email = StringField(required=True)
    username = StringField(required=True, max_length=20)
    password = StringField(required=True)

    def json(self):
        return {
            'id': self.id,
            'username': self.username
        }

    @classmethod
    def find_by_username(cls, username):
        return cls.objects(username=username).first()

    @classmethod
    def find_by_email(cls, email):
        return cls.objects(email=email).first()

    def save_to_db(self):
        self.save()

    def delete_from_db(self):
        self.delete()
