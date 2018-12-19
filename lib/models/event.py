from mongoengine import *

class EventModel(Document):
    """
        The abstract event class
    """
    
    title = StringField(required=True)
    text = StringField(required=True)
    user = StringField(required=True)
    location = StringField()
    date = DateTimeField()
    categories = ListField(StringField(max_length=20))
    meta = {'allow_inheritance':True}
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

class OfferModel(EventModel):
    """
        The model for offers made by viewers to performers
    """

    size = StringField()
    requirements = StringField()
    compensation = StringField()
    status = StringField()
    applicants = ListField(StringField(max_length=20))
    approved_performers = ListField(StringField(max_length=20))

class PerformanceModel(EventModel):
    """
        The model for offers made by performers to viewers
    """
    
    performer = StringField()
    collaborators = ListField(StringField())
    categories = ListField(StringField())
