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
        user = User(username="Juan", email="juan@a.a")
        db.session.add(user)
        db.session.commit()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f"<User {self.username}>"


class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        include_relationships = True
        load_instance = True
        sqla_session = db.session
