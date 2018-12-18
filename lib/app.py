from flask import Flask, jsonify
from flask_bcrypt import Bcrypt
from flask_restful import Api
from mongoengine import connect
import datetime
from resources.user import UserLogin, TokenRefresh, PerformerRegister, AdmirerRegister, UserLogout, RevokeRefreshToken
from resources.event import Event, EventList
from resources.offer import Offer, OfferList
from resources.performer import Performer
from flask_jwt_extended import JWTManager 
import redis

app = Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS'] = True

# ----------- SECURITY ------------

# ----------- Bcrypt

bcrypt = Bcrypt(app)

# ----------- JWT

# TO-DO: Secret key needs to be actually made secret, get it from enviroment
app.config['JWT_SECRET_KEY'] = "cute doggie"
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(days=1)
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
jwt = JWTManager(app)

revoked_store = redis.StrictRedis(host='localhost', port=6379, db=0,
decode_responses=True)

# Default routes needed for jwt handling
@jwt.expired_token_loader
def expired_token_callback():
    return jsonify({
        'message': 'The token has expired.',
        'error': 'token_expired'
    }), 401


@jwt.invalid_token_loader
def invalid_token_callback(error):  # we have to keep the argument here, since it's passed in by the caller internally
    return jsonify({
        'message': 'Signature verification failed.',
        'error': 'invalid_token'
    }), 401


@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({
        "description": "Request does not contain an access token.",
        'error': 'authorization_required'
    }), 401


@jwt.needs_fresh_token_loader
def token_not_fresh_callback():
    return jsonify({
        "description": "The token is not fresh.",
        'error': 'fresh_token_required'
    }), 401


@jwt.revoked_token_loader
def revoked_token_callback():
    return jsonify({
        "description": "The token has been revoked.",
        'error': 'token_revoked'
}), 401


@jwt.token_in_blacklist_loader
def check_if_token_is_revoked(decrypted_token):
    jti = decrypted_token['jti']
    entry = revoked_store.get(jti)
    if entry is None:
        return True
    return entry == 'true'
# ----------- DATABASE -----------

# ----------- MONGODB
app.config["MONGODB_DB"] = 'Minstrel'
connect(
    'Minstrel'
)
#TO-DO: Secret key needs to be secret, move to enviroment
app.secret_key = 'doggo'

# ----------- ROUTES -----------

# ----------- API 
api = Api(app)

api.add_resource(AdmirerRegister, '/register/admirer')
api.add_resource(PerformerRegister, '/register/performer')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')
api.add_resource(RevokeRefreshToken, '/logout2')
api.add_resource(TokenRefresh, '/refresh')
api.add_resource(Event, '/event/<string:title>')
api.add_resource(EventList, '/event')
api.add_resource(Offer, '/offer/<string:title>')
api.add_resource(OfferList, '/offer')
api.add_resource(Performer, '/performer')

# ------------ MISC ------------

# Runs app if file is called
if __name__ == '__main__':
    app.run(debug=True) 
