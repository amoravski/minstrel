from mongoengine import *

class UserModel(Document):
    """
        The abstract user class
    """
    meta = {'allow_inheritance':True}
    
    email = StringField(required=True)
    username = StringField(required=True, max_length=20)
    password = StringField(required=True)

    def json(self):
        """Returns pretty json representation"""
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
    """
        The performer model - be wary, all classmethods only apply to other performers
    """
    tags = ListField(StringField(max_length=20))

class ViewerModel(UserModel):
    """
        The viewer model - be wary, all classmethods only apply to other viewers
    """
    favorites = ListField(StringField(max_length=20))
