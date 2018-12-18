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

    categories = ListField(StringField(max_length=20))
    description = StringField(max_length=300)
    performances = ListField(StringField(max_length=20))
    collaborators = ListField()
    contacts = DictField()
    
    # Media, stored locally
    profile_picture = StringField()
    highlights = ListField(StringField())
    
    # Location, stored as lat and lon
    location = GeoPointField()

    # Settings
    settings = DictField(default={
        "public_email?": "false",
        "show_location?": "false",
        "recieve_offers?": "false",
        "offer_notifications?": "false",
        "collaborations?": "false",
                }
            )

    @staticmethod
    def is_category_allowed(category):
        acceptable_categories = [
                "musician",
                "dancer",
                "singer",
                "artist",
                "comedian",
                "living statue",
                "one-person band",
                "mime",
                "clown",
                "jongleur",
                "acrobat",
                "magician",
                "puppeteer",
                "improviser",
                "charicaturist",
                "animal tamer",
                "snake-charmer",
                "fire eater",
                "sword swallower",
                "storyteller",
                "ensemble",
                "other",
                ]
        if category in acceptable_categories:
            return True
        else:
            return False

class AdmirerModel(UserModel):
    """
        The admirer model - be wary, all classmethods only apply to other viewers
    """

    preferences = ListField(StringField(max_length=20))
    favorites = ListField(StringField(max_length=20))
    contacts = DictField()

    # Media, stored locally
    profile_picture = StringField()
 
    # Settings

    settings = DictField(default={
        "public_email?": "false"
                }
            )


