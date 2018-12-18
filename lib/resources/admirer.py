from flask_restful import Resource
from flask_jwt_extended import (jwt_required, get_jwt_identity)
from models.user import AdmirerModel
from resources.parsers import admirer_settings_parser
from json import loads
class Admirer(Resource):
    '''
        The admirer API
    '''
    
    @jwt_required
    def get(self):
        current_user = get_jwt_identity()
        admirer = AdmirerModel.find_by_email(current_user)
        if not admirer:
            return {"status":"error", "message":"User is not admirer"}
        return {"status": "ok", "user": admirer.json()}, 200

    @jwt_required
    def put(self):
        current_user = get_jwt_identity()
        data = admirer_settings_parser.parse_args()
        admirer = AdmirerModel.find_by_email(current_user)
        if not admirer:
            return {"status":"error", "message":"User is not admirer"}
        for setting in admirer.settings:
            result = set_setting(admirer, setting, data)
            if result['status'] == "ok":
                admirer = result['admirer']
            else:
                return result, 400

        admirer.save()
        return {"status": "ok", "message": "All good"}, 200
    
def set_setting(admirer, setting, data):
    if data['settings'].get(setting, False) and data['settings'].get(setting) in ['true', 'false']:
        admirer.settings[setting] = data['settings'][setting]
        return {"status": "ok", "admirer": admirer}
    else:
        return {"status": "error", "message": "Unrecognized setting"}

