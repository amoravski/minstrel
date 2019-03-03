from flask import request
from flask_restful import Resource
from flask_jwt_extended import (jwt_required, get_jwt_identity, jwt_optional)
from flask_bcrypt import generate_password_hash
from models.user import UserModel, PerformerModel
from models.event import PerformanceModel
from resources.parsers import performer_parser, performer_settings_parser
from json import loads
class Performer(Resource):
    """
        Performer API - GET is public, everything else is private to performer
    """
    
    @jwt_required
    def get(self, username):
        performer = PerformerModel.find_by_username(username)
        if not performer:
            return {'status':'error', 'message':'User is not performer'}, 403
        
        json = performer.json()
        performances_titles = []
        for uuid in json['performances']:
            title = PerformanceModel.find_by_uuid(uuid).title
            performances_titles.append(title)
        json['performances'] = performances_titles
        return {'status': 'ok', 'user': json}, 200

    @jwt_required
    def patch(self, username):
        performer = PerformerModel.find_by_username(username)
        user = get_jwt_identity()

        # Check first if performer exists, then check if the requester is this performer
        if not performer or not user == performer.email:
            return {'status':'error', 'message':'No such performer exists or user is not requested performer'}, 403
        
        # Parse args
        data = performer_settings_parser.parse_args()
        return_message = []

        # Username
        if data['username']:
            if PerformerModel.find_by_username(data['username']):
                return {'status':'error', 'message':'Username taken'}, 403
            performer.username = data['username']
            return_message.append('username')

        # Password
        if data['password']:
            password_hash = generate_password_hash(data['password']).decode('utf-8')
            performer.password = password_hash
            return_message.append('password')

        # Categories
        if data['categories']:
            filter_response = PerformerModel.filter_categories(data['categories'])
            if filter_response['status'] == 'error':
                return filter_response, 403
            performer.categories = filter_response['categories']
            return_message.append('categories')

        # Description
        if data['description']:
            performer.description = data['description']
            return_message.append('description')

        # Settings
        if data['settings']:
            for setting in performer.settings:
                result = set_setting(performer, setting, data)
                if result['status'] == 'ok':
                    performer = result['performer']
                else:
                    return result, 403
            return_message.append('settings')

        try:
            performer.save_to_db()
        except:
            return {'status': 'error', 'message': 'Something went wrong'}, 500

        return {'status': 'ok', 'changed:': return_message}, 200
    
class PerformerRegister(Resource):
    """
        Performer creation. Seperated because it takes name from body parameters
    """

    def post(self):
        data = performer_parser.parse_args()

        errors = {}
        # Calls UserModel to search through all users, not just performers
        if UserModel.find_by_email(data['email']):
            errors['email'] =  'A user with this email already exists'
        if UserModel.find_by_username(data['username']):
            errors['username'] =  'A user with this username already exists'

        # Bcrypt hash
        password_hash = generate_password_hash(data['password']).decode('utf-8')

        # Checks if categories are valid
        filter_response = PerformerModel.filter_categories(data['categories'])
        if filter_response['status'] == 'error':
            errors["categories"] = filter_response['message']

        if errors:
            errors['status'] = 'error'
            return errors, 403

        provided_location = data['location']
        result_location = [float(provided_location[0]), float(provided_location[1])]

        performer = PerformerModel(data['email'], data['username'], password_hash, result_location, filter_response['categories'])

        try:
            performer.save_to_db()
        except Exception as e:
            return {'status': 'error', 'message': str(e)}, 500

        return {'status': 'ok','message': 'Performer created successfully.'}, 201

class PerformerList(Resource):
    """
        Resource for getting a list of performers, only get is allowed
    """

    def get(self):
        performers_json = []
        
        if request.args.getlist('categories'):
            categories = request.args.getlist('categories')
            for performer in PerformerModel.find_by_categories(categories):
                performer_no_uuids = performer.json()
                del performer_no_uuids['performances']
                performers_json.append(performer_no_uuids)
        else:
            for performer in PerformerModel.find_all():
                performer_no_uuids = performer.json()
                del performer_no_uuids['performances']
                performers_json.append(performer_no_uuids)
        
        return {'status': 'ok', 'performers': performers_json}


def set_setting(performer, setting, data):
    """
        Function has been moved out for readability, intended only for this module
    """

    if data['settings'].get(setting, False) and data['settings'].get(setting) in ['true', 'false']:
        performer.settings[setting] = data['settings'][setting]
        return {'status': 'ok', 'performer': performer}
    else:
        return {'status': 'error', 'message': 'Unrecognized setting'}

