from mongoengine import *

class UserModel(Document):
    meta = {'allow_inheritance':True}
    email = StringField(required=True)
    username = StringField(required=True, max_length=20)
    password = StringField(required=True)

    def json(self):
        return {
            'email': self.email,
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


class PerformerModel(UserModel):
    tags = ListField(StringField(max_length=20))

class ViewerModel(UserModel):
    favorites = ListField(StringField(max_length=20))
