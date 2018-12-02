from mongoengine import *

class EventModel(Document):
    """
        Created by performers, for big collaborations or announcments
    """
    
    title = StringField(required=True)
    text = StringField(required=True)
    user = StringField(required=True)

    def json(self):
        """Returns pretty json representation"""
        return {
                "title": self.title,
                "text": self.text,
                "user": self.user
                }


    @classmethod
    def find_by_title(cls, title):
        return cls.objects(title=title).first()

    @classmethod
    def find_by_user(cls, user):
        return cls.objects(user=user).all()

    @classmethod
    def find_all(cls):
        return cls.objects().all()

    def save_to_db(self):
        self.save()

    def delete_from_db(self):
        self.delete()
