from flask import request
from flask_restful import Resource
from flask_jwt_extended import (jwt_required, get_jwt_identity, jwt_optional)
from flask_bcrypt import generate_password_hash
from models.user import UserModel, PerformerModel
from models.event import PerformanceModel
from resources.parsers import performer_parser, performer_settings_parser
from json import loads
class Performer(Resource):
    '''
        The performer API
    '''
    
    @jwt_required
    def get(self, username):
        performer = PerformerModel.find_by_username(username)
        if not performer:
            return {"status":"error", "message":"User is not performer"}
        
        json = performer.json()
        performances_titles = []
        for uuid in json['performances']:
            title = PerformanceModel.find_by_uuid(uuid).title
            performances_titles.append(title)
        json['performances'] = performances_titles
        return {"status": "ok", "user": json}, 200

    @jwt_required
    def patch(self, username):
        performer = PerformerModel.find_by_username(username)
        if not performer:
            return {"status":"error", "message":"User is not performer"}
        
        data = performer_settings_parser.parse_args()
        return_message = []
        #Username
        if data["username"]:
            if PerformerModel.find_by_username(data["username"]):
                return {"status":"error", "message":"Username taken"}
            performer.username = data["username"]
            return_message.append("username")
        #Password
        if data["password"]:
            password_hash = generate_password_hash(data['password']).decode('utf-8')
            performer.password = password_hash
            return_message.append("password")

        #Categories
        if data["categories"]:
            filter_response = PerformerModel.filter_categories(data['categories'])
            if filter_response['status'] == "error":
                return filter_response
            performer.categories = filter_response["categories"]
            return_message.append("categories")


        #Description
        if data['description']:
            performer.description = data['description']
            return_message.append("description")

        #Settings
        if data["settings"]:
            for setting in performer.settings:
                result = set_setting(performer, setting, data)
                if result['status'] == "ok":
                    performer = result['performer']
                else:
                    return result, 400
            return_message.append("settings")

        performer.save()
        return {"status": "ok", "changed:": return_message}, 200
    
class PerformerRegister(Resource):
    def post(self):
        data = performer_parser.parse_args()

        # Calls UserModel to search through all users, not just performers
        if UserModel.find_by_email(data['email']):
            return {"message": "A user with this email already exists"}, 400
        if UserModel.find_by_username(data['username']):
            return {"message": "A user with this username already exists"}, 400

        # Bcrypt hash
        password_hash = generate_password_hash(data['password']).decode('utf-8')


        filter_response = PerformerModel.filter_categories(data['categories'])
        if filter_response['status'] == "error":
            return filter_response

        performer = PerformerModel(data['email'], data['username'], password_hash, data['location'], filter_response['categories'])

        performer.save_to_db()

        return {"status": "ok","message": "Performer created successfully."}, 201

class PerformerList(Resource):
    def get(self):
        categories = request.args.getlist('categories')
        performers_json = []
        for performer in PerformerModel.find_by_categories(categories):
            performer_no_uuids = performer.json()
            del performer_no_uuids["performances"]
            performers_json.append(performer_no_uuids)
        return {"status": "ok", "performers": performers_json}

def set_setting(performer, setting, data):
    if data['settings'].get(setting, False) and data['settings'].get(setting) in ['true', 'false']:
        performer.settings[setting] = data['settings'][setting]
        return {"status": "ok", "performer": performer}
    else:
        return {"status": "error", "message": "Unrecognized setting"}

