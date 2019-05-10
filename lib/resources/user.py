from flask_restful import Resource, reqparse
from pymongo import MongoClient
from models.user import UserModel
from flask_bcrypt import check_password_hash
from flask_jwt_extended import (create_access_token, create_refresh_token,
        jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt, get_jti)
from resources.parsers import user_parser
import redis

class UserLogin(Resource):
    def post(self):
        data = user_parser.parse_args()

        user = UserModel.find_by_email(data['email'])
        if user and check_password_hash(user['password'], data['password']):
            access_token = create_access_token(identity=user.email, fresh=True)
            refresh_token = create_refresh_token(identity=user.email)
            access_jti = get_jti(encoded_token=access_token)
            refresh_jti = get_jti(encoded_token=refresh_token)
            revoked_store = redis.StrictRedis(host='localhost', port=6379, db=0,
            decode_responses=True)
            revoked_store.set(access_jti, 'false')
            revoked_store.set(refresh_jti, 'false')

            if (user._cls == "UserModel.PerformerModel"):
                return {'status': 'ok','access_token': access_token, 'refresh_token': refresh_token, 'type': "Performer"}, 200
            elif (user._cls == "UserModel.AdmirerModel"):
                return {'status': 'ok','access_token': access_token, 'refresh_token': refresh_token, 'type': "Admirer"}, 200
            elif (user._cls == "UserModel.AdministratorModel"):
                return {'status': 'ok','access_token': access_token, 'refresh_token': refresh_token, 'type': "Administrator"}, 200
        else:
            return {'status': 'error','message': 'invalid email or password'}, 401

class UserLogout(Resource):
    @jwt_required
    def delete(self):
        revoked_store = redis.StrictRedis(host='localhost', port=6379, db=0,
decode_responses=True)
        jti = get_raw_jwt()['jti']
        revoked_store.set(jti, 'true')
        return {'status': 'ok', 'message': 'Access token revoked'}, 200

class RevokeRefreshToken(Resource):
    @jwt_refresh_token_required
    def delete(self):
        revoked_store = redis.StrictRedis(host='localhost', port=6379, db=0,
decode_responses=True)
        jti = get_raw_jwt()['jti']
        revoked_store.set(jti, 'true')
        return {'status': 'ok', 'message': 'Access token revoked'}, 200


class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {'status': 'ok', 'access_token': new_token}, 200
