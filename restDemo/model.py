from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from sqlalchemy_utils import database_exists
import os

db = SQLAlchemy()


def init_db(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{app.root_path}/flask.db"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    if not database_exists(app.config['SQLALCHEMY_DATABASE_URI']):
        db.create_all(app=app)
        seed_db(app)


def seed_db(app):
    with app.app_context():
        users = [ User(username="juan", email="juan@a.a"),
                  User(username="maria", email="maria@a.a"),
                ]
        owners = [ Owner(name="Juan Pérez", user=users[0]),
                   Owner(name="María López", user=users[1])
                 ]
        pets = [ Pet(name="Estrella", species="Perro", breed="Caniche", owner=owners[0]),
                 Pet(name="Petardo", species="Perro", breed="Galgo", owner=owners[1]),
                 Pet(name="Nala", species="Perro", breed="Galgo", owner=owners[1]),
                 Pet(name="Mora", species="Gato", breed="Egipcio", owner=owners[1]),
                 ]
        for user in users:
            db.session.add(user)
        for owner in owners:
            db.session.add(owner)
        for pet in pets:
            db.session.add(pet)
        db.session.commit()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    ## se puede declarar la relación en ambos lados usando backref
    ## si se usara back_populates es necesario declararla en ambos lados
    #user = db.relationship("Owner", backref=db.backref("user", uselist=False))

    def __repr__(self):
        return f"<User {self.username}>"


class Owner(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    # TODO: test cascade behaviour
    user = db.relationship("User", backref=db.backref("owner", uselist=False))

    def __repr__(self):
        return f"<User {self.name}>"


class Pet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    species = db.Column(db.String(80), unique=False, nullable=True)
    breed = db.Column(db.String(80), unique=False, nullable=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('owner.id'))
    # TODO: test cascade behaviour
    owner = db.relationship("Owner", backref="pets")

    def __repr__(self):
        return f"<User {self.name}>"






###
# Marshmallow schemas definition
class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        include_relationships = True
        load_instance = True
        sqla_session = db.session


class OwnerSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Owner
        include_relationships = True
        load_instance = True
        sqla_session = db.session


class PetSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Pet
        include_relationships = True
        load_instance = True
        sqla_session = db.session