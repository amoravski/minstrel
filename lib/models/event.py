from mongoengine import *

class EventModel(Document):
    """
        The abstract event class
    """
    
    title = StringField(required=True, max_length=50)
    text = StringField(required=True, max_length=500)
    user = StringField(required=True, max_length=100)
    location = StringField(max_length=100)
    date = IntField(max_length=20)
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
    def json(self):
        return {
                "title": self.title,
                "text": self.text,
                "owner": self.user,
                "location": self.location,
                "date": self.date,
                "categories": self.categories,
                "size": self.size,
                "type_of_event": self.type_of_event,
                "requirements": self.requirements,
                "compensation": self.compensation,
                "status": self.status
                }
    size = StringField(max_length=20)
    type_of_event = StringField(max_length=20)
    requirements = StringField(max_length=300)
    compensation = StringField(max_length=300)
    status = StringField(default="Active")
    applicants = ListField(StringField(max_length=20))
    approved_performers = ListField(StringField(max_length=20))

class PerformanceModel(EventModel):
    """
        The model for offers made by performers to viewers
    """
    
    performer = StringField()
    collaborators = ListField(StringField())
    categories = ListField(StringField())
