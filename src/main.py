"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

#Método GET#
@app.route('/user', methods=['GET'])
def handle_hello():
    people_query = User.query.all()
    all_people = list(map(lambda x: x.serialize(), people_query))
    return jsonify(all_people), 200

@app.route('/user/<id>', methods=["GET"])
def busqueda_usuario(id):
    user1 = User.query.filter_by(id=id).first()
    if user1 is None:
        return APIException("No se encontro el usuario",status_code=404)
    request_body = user1.serialize()
    return jsonify(request_body),200


#Método POST#
@app.route('/user', methods=['POST'])
def create_user():
    data = request.get_json()
    user1 = User(email=data["email"],password=data["password"]) #is_active=data["is_active"]
    db.session.add(user1)
    db.session.commit()
    return jsonify ("Message : Se adiciono un usuario!"), 200
  #  return jsonify({user1}), 200

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
