from flask import request
from flask_restful import Resource
from flask_jwt_extended import (jwt_required, get_jwt_identity, jwt_optional)
from models.user import UserModel, PerformerModel, AdmirerModel
from models.event import PerformanceModel, OfferModel, EventModel
from resources.parsers import administrator_action_parser
from json import loads
class AdministratorActions(Resource):
    """
        Admin actions API
    """

    @jwt_required
    def get(self):
        """
            Returns a list of accounts and posts
        """
        performers = []
        for performer in PerformerModel.find_all():
            performer_no_uuids = performer.json()
            del performer_no_uuids['performances']
            performers.append(performer_no_uuids)

        admirers = []
        for admirer in AdmirerModel.find_all():
            admirer_no_uuids = admirer.json()
            del admirer_no_uuids['offers']
            admirers.append(admirer_no_uuids)

        performances = []
        for performance in PerformanceModel.find_all():
            #performance_no_uuid = performance.json()
            performances.append(performance.json())

        offers = []
        for offer in OfferModel.find_all():
            #offer_no_uuids = admirer.json()
            offers.append(offer.json())

        return {
                "status": "OK",
                "performers": performers,
                "admirers": admirers,
                "offers": offers,
                "performances": performances,
                }, 200


    @jwt_required
    def delete(self):
        """
            Deletes a post or account
        """
        data = administrator_action_parser.parse_args()

        if (data["type"] == "account"):
            if UserModel.find_by_email(data["identifier"]):
                UserModel.find_by_email(data["identifier"]).delete_from_db()
                return {
                    "status": "OK",
                    "message": "User deleted"
                    }
            return {
                    "status": "Error",
                    "message": "User not found"
                    }
        elif (data["type"] == "event"):
            if EventModel.find_by_title(data["identifier"]):
                EventModel.find_by_title(data["identifier"]).delete_from_db()
                return {
                    "status": "OK",
                    "message": "Event deleted"
                    }
            return {
                    "status": "Error",
                    "message": "Event not found"
                    }
        return {
                "status": "Error",
                "message": "Invalid type"
                }
