from flask_restful import Resource, reqparse
from flask_jwt_extended import get_jwt_identity, jwt_required, get_jwt_claims, fresh_jwt_required, jwt_optional
from models.event import OfferModel

class Offer(Resource):
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
        offer = OfferModel.find_by_title(title)
        if offer:
            return offer.json()
        return {'message': 'Offer not found'}, 404

    @fresh_jwt_required
    def post(self, title):
        if OfferModel.find_by_title(title):
            return {'message': "An Offer with name '{}' already exists.".format(title)}, 400

        data = self.parser.parse_args()

        user_id = get_jwt_identity()
        offer = OfferModel(title, data['text'], user_id)

        try:
            offer.save_to_db()
        except:
            return {"message": "An error occurred while creating the offer."}, 500

        return offer.json(), 201
