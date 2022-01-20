from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from sqlalchemy_utils import database_exists

db = SQLAlchemy()

# db initialization (no change)
def init_db(app, guard):
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{app.root_path}/flask.db"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    if not database_exists(app.config['SQLALCHEMY_DATABASE_URI']):
        db.create_all(app=app)
        seed_db(app, guard)


# seeding database with test data
def seed_db(app, guard):
    with app.app_context():
        users = [
            User(username="juan", email="juan@a.a", hashed_password=guard.hash_password("pestillo"), roles="admin"),
            User(username="maria", email="maria@a.a", hashed_password=guard.hash_password("pestillo"), roles="admin"),
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

# classes for model entities
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    ## se puede declarar la relación en ambos lados usando backref
    ## si se usara back_populates es necesario declararla en ambos lados
    #user = db.relationship("Owner", backref=db.backref("user", uselist=False))
    # from praetorian example
    hashed_password = db.Column(db.Text)
    roles = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True, server_default="true")

    @property
    def identity(self):
        """
        *Required Attribute or Property*

        flask-praetorian requires that the user class has an ``identity`` instance
        attribute or property that provides the unique id of the user instance
        """
        return self.id

    @property
    def rolenames(self):
        """
        *Required Attribute or Property*

        flask-praetorian requires that the user class has a ``rolenames`` instance
        attribute or property that provides a list of strings that describe the roles
        attached to the user instance
        """
        try:
            return self.roles.split(",")
        except Exception:
            return []

    @property
    def password(self):
        """
        *Required Attribute or Property*

        flask-praetorian requires that the user class has a ``password`` instance
        attribute or property that provides the hashed password assigned to the user
        instance
        """
        return self.hashed_password

    @classmethod
    def lookup(cls, username):
        """
        *Required Method*

        flask-praetorian requires that the user class implements a ``lookup()``
        class method that takes a single ``username`` argument and returns a user
        instance if there is one that matches or ``None`` if there is not.
        """
        return cls.query.filter_by(username=username).one_or_none()

    @classmethod
    def identify(cls, id):
        """
        *Required Method*

        flask-praetorian requires that the user class implements an ``identify()``
        class method that takes a single ``id`` argument and returns user instance if
        there is one that matches or ``None`` if there is not.
        """
        return cls.query.get(id)

    def is_valid(self):
        return self.is_active

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
