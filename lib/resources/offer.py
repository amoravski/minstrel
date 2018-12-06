from flask_restful import Resource, reqparse
from flask_jwt_extended import get_jwt_identity, jwt_required, get_jwt_claims, fresh_jwt_required, jwt_optional
from models.event import OfferModel
from resources.parsers import offer_parser

class Offer(Resource):
    """
        Methods by which events are made possible
    """

    def get(self, title):
        offer = OfferModel.find_by_title(title)
        if offer:
            return offer.json()
        return {'message': 'Offer not found'}, 404

    @fresh_jwt_required
    def post(self, title):
        if OfferModel.find_by_title(title):
            return {'message': "An Offer with name '{}' already exists.".format(title)}, 400

        data = offer_parser.parse_args()

        user_id = get_jwt_identity()
        offer = OfferModel(title, data['text'], user_id)

        try:
            offer.save_to_db()
        except:
            return {"message": "An error occurred while creating the offer."}, 500

        return offer.json(), 201

class OfferList(Resource):
    """
        Returns a list of all offers
    """

    def get(self):
        offers = [offer.json() for offer in OfferModel.find_all()]
        return {'offers': offers}
