from flask_restful import Resource, reqparse
from flask_jwt_extended import get_jwt_identity, jwt_required, get_jwt_claims, fresh_jwt_required, jwt_optional
from models.event import PerformanceModel
from models.user import PerformerModel
from resources.parsers import performance_parser, performance_setting_parser
from uuid import uuid4
from time import time

class Performance(Resource):
    """
        Performance API - only GET method is public
    """

    def get(self, title):
        performance = PerformanceModel.find_by_title(title)
        if performance:
            return {'status':'ok', 'performer': performance.json()}
        return {'status': 'error', 'message': 'Performance not found'}, 404

    @fresh_jwt_required
    def post(self, title):
        user_id = get_jwt_identity()
        if not PerformerModel.find_by_email(user_id):
            return {'status': 'error', 'message': 'Only performers can make performances'}, 400
        if PerformanceModel.find_by_title(title):
            return {'status':'error','message': 'An Performance with name "{}" already exists.'.format(title)}, 400

        data = performance_parser.parse_args()

        performer_categories = PerformerModel.find_by_email(user_id).categories

        if not int(data['date'])>int(time()):
            return {'status': 'error', 'message': 'Date must be in the future'}, 400

        uuid = uuid4()
        performance = PerformanceModel(uuid, title, data['text'], user_id, data['location'], data['date'], performer_categories)

        performer = PerformerModel.find_by_email(user_id)
        performer.performances.append(uuid)
        try:
            performance.save_to_db()
            performer.save_to_db()
        except:
            return {'status': 'error','message': 'Something went wrong'}, 500

        return {'status': 'ok', 'performer': performance.json()}, 201

    @fresh_jwt_required
    def patch(self, title):
        performance = PerformanceModel.find_by_title(title)
        user = get_jwt_identity()                                                             

        # Check if performance already exists, check if user is owner
        if not performance or not user == performance.user:
            return {'status': 'error', 'message': 'No such performance found or user is not owner'}, 400

        # Parse args
        data = performance_setting_parser.parse_args()
        return_message = []

        # Title
        if data['title']:
            if PerformanceModel.find_by_title(data['title']):
                return {'status': 'error','message': 'An Performance with name "{}" already exists.'.format(data['title'])}, 400
            performance.title = data['title']
            return_message.append('title')

        # Text
        if data['text']:
            performance.text = data['text']
            return_message.append('text')

        # Location
        if data['location']:
            performance.location = data['location']
            return_message.append('location')
            
        # Date
        if data['date']:
            if not int(data['date'])>int(time()):
                return {'status': 'error', 'message': 'Date must be in the future'}, 400
            performance.date = data['date']
            return_message.append('date')

        try:
            performance.save()
        except:
            return {'status': 'error','message': 'Something went wrong'}, 500

        return {'status':'ok', 'changed:': return_message}

class PerformanceList(Resource):
    """
        Returns a list of all performances, only GET is allowed
    """

    def get(self):
        performances = [performance.json() for performance in PerformanceModel.find_all()]
        return {'status':'ok', 'performances': performances}
