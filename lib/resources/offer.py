from flask_restful import Resource, reqparse
from flask_jwt_extended import get_jwt_identity, jwt_required, get_jwt_claims, fresh_jwt_required, jwt_optional
from models.event import OfferModel
from resources.parsers import offer_parser, offer_setting_parser
from models.user import PerformerModel, AdmirerModel
from time import time
from uuid import uuid4

class Offer(Resource):
    """
        Offer API - only get is public
    """

    def get(self, title):
        offer = OfferModel.find_by_title(title)
        if offer:
            return {'status': 'ok', 'offer':offer.json()}, 200
        return {'status': 'error','message': 'Offer not found'}, 404

    @fresh_jwt_required
    def post(self, title):
        user_id = get_jwt_identity()
        if not AdmirerModel.find_by_email(user_id):
            return {'status': 'error', 'message': 'Only admirers can make offers'}, 400

        if OfferModel.find_by_title(title):
            return {'status': 'error','message': 'An offer with name {} already exists.'.format(title)}, 400

        data = offer_parser.parse_args()
        
        try:
            accepted_categories = PerformerModel.filter_categories(data['categories'])
            if accepted_categories['status'] == 'error':
                return accepted_categories
        except Exception as e:
            return {'status':'error', 'message': 'Something went wrong'}, 500
        
        if not int(data['date'])>int(time()):
            return {'status': 'error', 'message': 'Date must be in the future'}, 400
        
        uuid = uuid4()
        offer = OfferModel(
                uuid,
                title, 
                data['text'], 
                user_id, 
                data['location'], 
                data['date'], 
                accepted_categories['categories'],
                data['size'],
                data['type'],
                data['requirements'],
                data['compensation'],
                )

        admirer = AdmirerModel.find_by_email(user_id)
        admirer.offers.append(uuid)
        try:
            offer.save_to_db()
            admirer.save_to_db()
        except Exception as e:
            return {'status': 'error', 'message': 'Something went wrong'}, 500

        return {'status': 'ok','offer':offer.json()}, 201

    @fresh_jwt_required
    def patch(self, title):
        offer = OfferModel.find_by_title(title)
        user = get_jwt_identity()                                                             

        # Check if offer already exists, check if user is owner
        if not offer or not user == offer.user:
            return {'status': 'error', 'message': 'No such offer found or user is not owner'}, 400

        # Parse args
        data = offer_setting_parser.parse_args()
        return_message = []

        # Title
        if data['title']:
            if OfferModel.find_by_title(data['title']):
                return {'status':'error','message': 'An offer with name "{}" already exists.'.format(data['title'])}, 400
            offer.title = data['title']
            return_message.append('title')

        # Text
        if data['text']:
            offer.text = data['text']
            return_message.append('text')

        # Location
        if data['location']:
            offer.location = data['location']
            return_message.append('location')

        # Date
        if data['date']:
            if not int(data['date'])>int(time()):
                return {'status': 'error', 'message': 'Date must be in the future'}, 400
            offer.date = data['date']
            return_message.append('date')

        # Categories
        if data['categories']:
            filter_response = PerformerModel.filter_categories(data['categories'])
            if filter_response['status'] == 'error':
                return filter_response
            offer.categories = filter_response['categories']
            return_message.append('categories')

        # Type
        if data['type']:
            offer.location = data['type']
            return_message.append('type')

        # Requirements
        if data['requirements']:
            offer.location = data['requirements']
            return_message.append('requirements')

        # Compensation
        if data['compensation']:
            offer.location = data['compensation']
            return_message.append('compensation')

        # Size
        if data['size']:
            offer.location = data['size']
            return_message.append('size')

        try:
            offer.save()
        except:
            return {'status': 'error','message': 'Something went wrong'}, 500

        return {'status':'ok', 'changed:': return_message}

class OfferList(Resource):
    """
        Returns a list of offers, only GET is allowed
    """

    def get(self):
        offers = [offer.json() for offer in OfferModel.find_all()]
        return {'status':'ok','offers': offers}
