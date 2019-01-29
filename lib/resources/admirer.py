from flask_restful import Resource
from flask_jwt_extended import (jwt_required, get_jwt_identity, jwt_optional)
from flask_bcrypt import generate_password_hash
from models.user import UserModel, AdmirerModel, PerformerModel
from models.event import OfferModel
from resources.parsers import admirer_parser, admirer_settings_parser
from json import loads
class Admirer(Resource):
    """
        The admirer API, GET is public, PATCH is private
    """
    
    @jwt_required
    def get(self, username):
        admirer = AdmirerModel.find_by_username(username)
        if not admirer:
            return {'status':'error', 'message':'User is not admirer'}

        json = admirer.json()
        offers_titles = []
        for uuid in json['offers']:
            title = OfferModel.find_by_uuid(uuid).title
            offers_titles.append(title)
        json['offers'] = offers_titles

        return {'status': 'ok', 'user': json}, 200

    @jwt_required
    def patch(self, username):
        admirer = AdmirerModel.find_by_username(username)
        user = get_jwt_identity()

        # Check if admirer exists, check if requester is this admirer
        if not admirer or not user == admirer.email:
            return {'status':'error', 'message':'No such admirer exists or user is not requested performer'}, 400

        # Parse args
        data = admirer_settings_parser.parse_args()
        return_message = []
        # Username
        if data['username']:
            if AdmirerModel.find_by_username(data['username']):
                return {'status':'error', 'message':'Username taken'}, 400
            admirer.username = data['username']
            return_message.append('username')

        # Password
        if data['password']:
            password_hash = generate_password_hash(data['password']).decode('utf-8')
            admirer.password = password_hash
            return_message.append('password')

        # Preferences
        if data['preferences']:
            filter_response = PerformerModel.filter_categories(data['preferences'])
            if filter_response['status'] == 'error':
                return filter_response
            admirer.categories = filter_response['categories']
            return_message.append('preferences')

        # Settings
        for setting in admirer.settings:
            result = set_setting(admirer, setting, data)
            if result['status'] == 'ok':
                admirer = result['admirer']
            else:
                return result, 400
            return_message.append('settings')

        try:
            admirer.save_to_db()
        except:
            return{'status': 'error', 'message': 'Something went wrong'}, 500
        return {'status': 'ok', 'changed:': return_message}, 200

class AdmirerRegister(Resource):
    """
        Admirer creation. Seperated because it takes name from body parameters
    """

    def post(self):
        data = admirer_parser.parse_args()

        errors = {}
        # Calls UserModel to search through all users, not just admirers
        if UserModel.find_by_email(data['email']):
            errors['email'] =  'A user with this email already exists'
        if UserModel.find_by_username(data['username']):
            errors['username'] =  'A user with this username already exists'


        # Bcrypt hash
        password_hash = generate_password_hash(data['password']).decode('utf-8')

        filter_response = PerformerModel.filter_categories(data['categories'])
        if filter_response['status'] == 'error':
            errors["categories"] = filter_response['message']

        if errors:
            errors['status'] = 'error'
            return errors, 403

        admirer = AdmirerModel(data['email'], data['username'], password_hash, filter_response['categories'])
        try:
            admirer.save_to_db()
        except:
            return {'status': 'error','message': 'Something went wrong'}, 500
        return {'status': 'ok','message': 'Admirer created successfully.'}, 201
    
def set_setting(admirer, setting, data):
    """
        Function has been moved out for readability, intended only for this module
    """

    if data['settings'].get(setting, False) and data['settings'].get(setting) in ['true', 'false']:
        admirer.settings[setting] = data['settings'][setting]
        return {'status': 'ok', 'admirer': admirer}
    else:
        return {'status': 'error', 'message': 'Unrecognized setting'}

