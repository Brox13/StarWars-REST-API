import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Planetas, Personajes



app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)


@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_hello():
    user = User.query.all()
    listUser = list(map(lambda obj: obj.serialize(),user))
    response_body = {
        "result":listUser
    }
    return jsonify(response_body), 200

@app.route('/personajes', methods=['GET'])
def handle_personajes():
    personajes = Personajes.query.all()
    listPersonajes = list(map(lambda obj:obj.serialize(),personajes))
    response_body={
        "result":listPersonajes
    }
    return jsonify(response_body), 200
    
@app.route('/personajes/<int:id>', methods = ['GET'])
def handle_personaje():
    single_personajes = Personajes.query.get(id)
    characters = personaje.serialize()
    response_body = {
        "result":personajes
    }
    return jsonify(response_body), 200

@app.route('/planetas', methods=['GET'])
def handle_planetas():
    planetas = Planetas.query.all()
    listPlanetas = list(map(lambda obj:obj.serialize(),planetas))
    response_body={
        "result":listPlanetas
    }
    return jsonify(response_body), 200
    
@app.route('/planetas/<int:id>', methods = ['GET'])
def handle_planeta():
    single_planetas = Planetas.query.get(id)
    planetas = planeta.serialize()
    response_body = {
        "result":planetas
    }
    return jsonify(response_body), 200


@app.route('/user/favorite', methods = ['GET'])
def favorito_user(user_id):
    fav_personaje=User.query.filter_by(id=user_id).first().personajes
    fav_planeta= User.query.filter_by(id=user_id).first().planetas
    lista_favoritos=[]
    for i in fav_personaje:
        lista_favoritos.append(i.serialize())
    for x in fav_planeta:
        lista_favoritos.append(x.serialize())
    return jsonify(lista_favoritos), 200


@app.route('/favorito/planeta/<int:planeta_id>', methods=['POST'])
def add_fav_planeta(planetas_id):
    planet=Planetas.query.get(planetas_id)
    usuario=User.query.get(1)
    usuario.planetas.append(planet)
    db.session.commit()
    return jsonify({"succes":"planeta agregado"}), 200


@app.route('/favorit0/personaje/<int:personaje_id>', methods=['POST'])
def add_fav_personaje(personajes_id):
    personaje=Personajes.query.get(personajes_id)
    usuario=User.query.get(1)
    usuario.personajes.append(personaje)
    db.session.commit()
    return jsonify({"succes":"personaje agregado"}), 200

@app.route('/favorito/planeta/<int:planeta_id>', methods=['DELETE'])
def delete_fav_planeta(planetas_id):
    planeta= Planetas.query.get(planetas_id)
    usuario= User.query.get(1)
    usuario.planetas.remove(planeta)
    db.session.commit()
    return jsonify({"succes":"planeta eliminado"}), 200

@app.route('/favorito/personaje/<int:personaje_id>', methods=['DELETE'])
def delete_fav_personaje(personajes_id):
    personaje= Personajes.query.get(personajes_id)
    usuario= User.query.get(1)
    usuario.planetas.remove(planeta)
    db.session.commit()
    return jsonify({"succes":"planeta eliminado"}), 200



# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
