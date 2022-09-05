from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship

db = SQLAlchemy()

fav_personajes = db.Table('favorite_personajes',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'),primary_key=True),
    db.Column('personajes_id', db.Integer, db.ForeignKey('personajes.id', primary_key=True))
    )
fav_planetas = db.Table('favorite_planetas',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('planetas_id', db.Integer, db.ForeignKey('planetas.id'), primary_key=True)
    )
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    name = db.Column(db.String(250), nullable=False)
    last_name = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(250))
    personajes = relationship('Personajes', secondary=fav_personajes)
    planetas = relationship('Planetas', secondary=fav_planetas)
    def __repr__(self):
        return '<Users %r>' % self.username
    def serialize(self):
        return{
            "id":self.id,
            "username":self.username,
            "name":self.name,
            "last_name":self.last_name,
            "email":self.email,
            "rel_FavCharacters":self.rel_FavCharacters
        }

class Personajes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)

    def __repr__(self):
        return '<Personajes %r>' % self.name
    def serialize(self):
        return{
            "id":self.id,
            "name":self.name
        }
class Planetas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)

    def __repr__(self):
        return '<Planetas %r>' % self.name
    def serialize(self):
        return{
            "id":self.id,
            "name":self.name
        }