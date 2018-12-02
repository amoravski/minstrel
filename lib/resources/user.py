from flask_restful import Resource, reqparse
from flask_bcrypt import check_password_hash, generate_password_hash
from pymongo import MongoClient
from models.user import ViewerModel, PerformerModel, UserModel
from flask_jwt_extended import (create_access_token, create_refresh_token,
        jwt_required, jwt_refresh_token_required, get_jwt_identity)

parser = reqparse.RequestParser()
parser.add_argument('email',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
parser.add_argument('username',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
parser.add_argument('password',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
 
class PerformerRegister(Resource):
     def post(self):
        data = parser.parse_args()
        
        # Calls UserModel to search through all users, not just performers
        if UserModel.find_by_email(data['email']):
            return {"message": "A user with this email already exists"}, 400
        if UserModel.find_by_username(data['username']):
            return {"message": "A user with this username already exists"}, 400

        # Bcrypt hash
        password_hash = generate_password_hash(data['password']).decode('utf-8')

        performer = PerformerModel(data['email'], data['username'], password_hash)
        performer.save_to_db()

        return {"status": "ok","message": "Performer created successfully."}, 201

class ViewerRegister(Resource):
     def post(self):
        data = parser.parse_args()

        # Calls UserModel to search through all users, not just viewers
        if UserModel.find_by_email(data['email']):
            return {"message": "A user with this email already exists"}, 400
        if UserModel.find_by_username(data['username']):
            return {"message": "A user with this username already exists"}, 400

        # Bcrypt hash
        password_hash = generate_password_hash(data['password']).decode('utf-8')

        viewer = ViewerModel(data['email'], data['username'], password_hash)
        viewer.save_to_db()

        return {"status": "ok","message": "Viewer created successfully."}, 201


class UserLogin(Resource):
    def post(self):
        data = parser.parse_args()

        user = UserModel.find_by_email(data['email'])
        if user and check_password_hash(user['password'], data['password']):
            access_token = create_access_token(identity=user.email, fresh=True)
            refresh_token = create_refresh_token(identity=user.email)
            return {'access_token': access_token, 'refresh_token': refresh_token}, 200
        else:
            return {'status': 'error','message': 'invalid email or password'}, 401

class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {'access_token': new_token}, 200
