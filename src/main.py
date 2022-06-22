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
from models import db, User, Planets, People, Favorites
# from models import Person

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


# ............USUARIO.............................

@app.route('/user', methods=['GET'])
def handle_hello():

    user = User.query.all()
    list_user = list(map(lambda user: user.serialize(), user))
    return jsonify(list_user), 200

# .......................PERSONAJES...........................


@app.route('/people', methods=['GET'])
def all_people_get():
    people = People.query.all()
    list_people = list(map(lambda people: people.serialize(), people))
    return jsonify(list_people), 200


@app.route('/people/<int:id>', methods=['GET'])
def getpeople_id(id):

    people = People.query.filter_by(id=id).first()
    if people is None:
        raise APIException(
            "Message: Requested data not found.", status_code=404)
    request = people.serialize()
    return jsonify(request), 200

# ...................PLANETAS...............................


@app.route('/planets', methods=['GET'])
def all_planets_get():

    planets = Planets.query.all()
    list_planet = list(map(lambda planets: planets.serialize(), planets))
    return jsonify(list_planet), 200


@app.route('/planets/<int:id>', methods=['GET'])
def getPlanets_id(id):
    planets = Planets.query.filter_by(id=id).first()
    if planets is None:
        raise APIException(
            "Message: Requested data not found.", status_code=404)
    request = planets.serialize()
    return jsonify(request), 200

# .....................FAVORITOS................................


@app.route('/favorites/', methods=['GET'])
def get_favorites():

    favorite = Favorites.query.all()
    list_fav = list(map(lambda favorite: favorite.serialize(), favorite))
    return jsonify(list_fav), 200
# .....................POST  ................................


@app.route('/favorites/planet/<planet_id>', methods=['POST'])
def add_planet_fav(planet_id):

    body = request.get_json()
    user_id = body["user_id"]
    planet_id = body["planet_id"]

    planetfav = Favorites(
        user_id=user_id, planet_id=planet_id)
    db.session.add(planetfav)
    db.session.commit()
    return jsonify("ok"), 201


@app.route('/favorites/people/<people_id>', methods=['POST'])
def add_people_fav(people_id):

    body = request.get_json()
    user_id = body["user_id"]
    people_id = body["people_id"]

    peoplefav = Favorites(
        user_id=user_id, people_id=people_id)
    db.session.add(peoplefav)
    db.session.commit()
    return jsonify("ok"), 201

#  .....................DELETE ................................


@app.route('/favorites/planet/<planet_id>', methods=['DELETE'])
def delete_planet_fav(planet_id):

    planetfav = Favorites.query.get(planet_id)
    if planet_id is None:
        raise APIException("PLANET DELETE", 201)
    db.session.delete(planetfav)
    db.session.commit()

    return jsonify(planetfav.serialize())


@app.route('/favorites/people/<people_id>', methods=['DELETE'])
def delete_people_fav(people_id):

    peoplefav = Favorites.query.get(people_id)
    if people_id is None:
        raise APIException("PEOPLE DELETE", 201)
    db.session.delete(peoplefav)
    db.session.commit()

    return jsonify(peoplefav.serialize())


if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
