from flask_restful import Resource
from flask_jwt_extended import (jwt_required, get_jwt_identity)
from models.user import PerformerModel
from resources.parsers import performer_settings_parser
from json import loads
class Performer(Resource):
    '''
        The performer API
    '''
    
    @jwt_required
    def get(self):
        current_user = get_jwt_identity()
        performer = PerformerModel.find_by_email(current_user)
        return {"status": "ok", "user": performer.json()}, 200

    @jwt_required
    def put(self):
        current_user = get_jwt_identity()
        data = performer_settings_parser.parse_args()
        performer = PerformerModel.find_by_email(current_user)

        for setting in performer.settings:
            result = set_setting(performer, setting, data)
            if result['status'] == "ok":
                performer = result['performer']
            else:
                return result, 400

        performer.save()
        return {"status": "ok", "message": "All good"}, 200
    
def set_setting(performer, setting, data):
    if data['settings'].get(setting, False) and data['settings'].get(setting) in ['true', 'false']:
        performer.settings[setting] = data['settings'][setting]
        return {"status": "ok", "performer": performer}
    else:
        return {"status": "error", "message": "Unrecognized setting"}

