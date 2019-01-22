import os
from flask import Flask, jsonify, send_from_directory
from flask_bcrypt import Bcrypt
from flask_restful import Api
from mongoengine import connect
import datetime
from resources.user import UserLogin, TokenRefresh, UserLogout, RevokeRefreshToken
from resources.offer import Offer, OfferList
from resources.performance import Performance, PerformanceList
from resources.performer import Performer, PerformerRegister, PerformerList
from resources.admirer import Admirer, AdmirerRegister
from flask_jwt_extended import JWTManager 
import redis

app = Flask(__name__, static_folder='../front_end/build')
app.config['PROPAGATE_EXCEPTIONS'] = True

# Serve React App
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists("../front_end/build/" + path):
        return send_from_directory('../front_end/build', path)
    else:
        return send_from_directory('../front_end/build', 'index.html')

# ----------- SECURITY ------------

# ----------- Bcrypt

bcrypt = Bcrypt(app)

# ----------- JWT

# TO-DO: Secret key needs to be actually made secret, get it from enviroment
app.config['JWT_SECRET_KEY'] = 'cute doggie'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(days=1)
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
jwt = JWTManager(app)

# Redis storage for jwt status
revoked_store = redis.StrictRedis(host='localhost', port=6379, db=0,
decode_responses=True)

# Default routes needed for jwt handling
@jwt.expired_token_loader
def expired_token_callback():
    return jsonify({
        'status': 'error',
        'message': 'The token has expired.',
    }), 401


@jwt.invalid_token_loader
def invalid_token_callback(error):  # we have to keep the argument here, since it's passed in by the caller internally
    return jsonify({
        'status': 'error',
        'message': 'Signature verification failed.',
    }), 401


@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({
        'status': 'error',
        'message': 'Request does not contain an access token.',
    }), 401


@jwt.needs_fresh_token_loader
def token_not_fresh_callback():
    return jsonify({
        'status': 'error',
        'message': 'The token is not fresh.',
    }), 401


@jwt.revoked_token_loader
def revoked_token_callback():
    return jsonify({
        'status': 'error',
        'message': 'The token has been revoked.',
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
app.config['MONGODB_DB'] = 'Minstrel'
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
api.add_resource(Offer, '/offer/<string:title>')
api.add_resource(OfferList, '/offer')
api.add_resource(Performance, '/performance/<string:title>')
api.add_resource(PerformanceList, '/performance')
api.add_resource(Performer, '/performer/<string:username>')
api.add_resource(PerformerList, '/performer')
api.add_resource(Admirer, '/admirer/<string:username>')
# ------------ MISC ------------

# Runs app if file is called
if __name__ == '__main__':
    app.run(debug=True) 
