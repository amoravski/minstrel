from flask_restful import Resource, reqparse
from flask_jwt_extended import get_jwt_identity, jwt_required, get_jwt_claims, fresh_jwt_required, jwt_optional
from models.event import OfferModel
from resources.parsers import offer_parser
from models.user import PerformerModel, AdmirerModel
from time import time
from uuid import uuid4

class Offer(Resource):
    """
        Methods by which events are made possible
    """

    def get(self, title):
        offer = OfferModel.find_by_title(title)
        if offer:
            return offer.json()
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
            if accepted_categories['status'] == "error":
                return accepted_categories
        except Exception as e:
            return {'status':'error', 'message': 'Something went wrong when processing parameters' + str(e)}, 500
        
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
            return {'status': 'error', 'message': 'Something went wrong when processing parameters'}, 500

        return offer.json(), 201

class OfferList(Resource):
    """
        Returns a list of all offers
    """

    def get(self):
        offers = [offer.json() for offer in OfferModel.find_all()]
        return {'offers': offers}
