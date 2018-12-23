from flask_restful import Resource
from flask_jwt_extended import (jwt_required, get_jwt_identity, jwt_optional)
from flask_bcrypt import generate_password_hash
from models.user import UserModel, AdmirerModel, PerformerModel
from models.event import OfferModel
from resources.parsers import admirer_parser, admirer_settings_parser
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

        json = admirer.json()
        offers_titles = []
        for uuid in json['offers']:
            title = OfferModel.find_by_uuid(uuid).title
            offers_titles.append(title)
        json['offers'] = offers_titles

        return {"status": "ok", "user": json}, 200

    @jwt_required
    def put(self):
        current_user = get_jwt_identity()
        data = admirer_settings_parser.parse_args()
        admirer = AdmirerModel.find_by_email(current_user)
        if not admirer:
            return {"status":"error", "message":"User is not admirer"}

        #Settings
        for setting in admirer.settings:
            result = set_setting(admirer, setting, data)
            if result['status'] == "ok":
                admirer = result['admirer']
            else:
                return result, 400

        admirer.save()
        return {"status": "ok", "message": "All good"}, 200

class AdmirerRegister(Resource):
     def post(self):
        data = admirer_parser.parse_args()

        # Calls UserModel to search through all users, not just admirers
        if UserModel.find_by_email(data['email']):
            return {"message": "A user with this email already exists"}, 400
        if UserModel.find_by_username(data['username']):
            return {"message": "A user with this username already exists"}, 400

        # Bcrypt hash
        password_hash = generate_password_hash(data['password']).decode('utf-8')

        filter_response = PerformerModel.filter_categories(data['preferred_categories'])
        if filter_response['status'] == "error":
            return filter_response

        admirer = AdmirerModel(data['email'], data['username'], password_hash, filter_response['categories'])
        admirer.save_to_db()

        return {"status": "ok","message": "Admirer created successfully."}, 201
    
def set_setting(admirer, setting, data):
    if data['settings'].get(setting, False) and data['settings'].get(setting) in ['true', 'false']:
        admirer.settings[setting] = data['settings'][setting]
        return {"status": "ok", "admirer": admirer}
    else:
        return {"status": "error", "message": "Unrecognized setting"}

