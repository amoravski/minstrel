from flask_restful import Resource, reqparse
from flask_jwt_extended import get_jwt_identity, jwt_required, get_jwt_claims, fresh_jwt_required, jwt_optional
from models.event import EventModel


"""
The following resources contain endpoints that are protected by jwt,
one may need a valid access token, a valid fresh token or a valid token with authorized privilege 
"""


class Event(Resource):
    """
        Methods by which events are made possible
    """
    parser = reqparse.RequestParser()
    parser.add_argument('text',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    def get(self, title):
        event = EventModel.find_by_title(title)
        if event:
            return event.json()
        return {'message': 'Event not found'}, 404

    @fresh_jwt_required
    def post(self, title):
        if EventModel.find_by_title(title):
            return {'message': "An Event with name '{}' already exists.".format(title)}, 400

        data = self.parser.parse_args()

        user_id = get_jwt_identity()
        event = EventModel(title, data['text'], user_id)

        try:
            event.save_to_db()
        except:
            return {"message": "An error occurred while creating the event."}, 500

        return event.json(), 201

    @jwt_required
    def delete(self, name):
        claims = get_jwt_claims()
        if not claims['is_admin']:
            return {'message': 'Admin privilege required.'}, 401

        event = EventModel.find_by_title(title)
        if event:
            event.delete_from_db()
            return {'message': 'Event deleted.'}
        return {'message': 'Event not found.'}, 404

    #TO-DO: Make put method work
    def put(self, name):
        data = self.parser.parse_args()

        event = EventModel.find_by_name(name)

        if event:
            event.people = data['price']
        else:
            event = ItemModel(name, **data)

        event.save_to_db()

        return event.json()


class EventList(Resource):
    @jwt_optional
    def get(self):
        user_id = get_jwt_identity()
        events = [event.json() for event in EventModel.find_all()]
        if user_id:
            return {'events': events}, 200
        return {
            'items': [event['title'] for event in events],
            'message': 'More data available if you log in.'
}, 200
