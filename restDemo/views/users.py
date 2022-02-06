import flask_praetorian
from flask import request, jsonify, current_app
from flask_restx import abort, Resource, Namespace

from sqlalchemy.sql import text
from model import User, db, UserSchema

# namespace declaration
api_user = Namespace("Users", "Users management")


@api_user.route("/<user_id>")
class UserController(Resource):
    # methods for http methods supported
    # auth required
    @flask_praetorian.auth_required
    def get(self, user_id):
        # gets one user by id
        user = User.query.get_or_404(user_id)
        # UserSchema() is an object used for ORM objects serialization
        return UserSchema().dump(user)

    # roles required (if several roles, user must have every role)
    @flask_praetorian.roles_required("admin")
    def delete(self, user_id):
        user = User.query.get_or_404(user_id)
        # delete user
        db.session.delete(user)
        # commit needed after every writing operation (not query)
        db.session.commit()
        # using 204 response code
        return f"Deleted user {user_id}", 204

    @flask_praetorian.roles_required("admin")
    def put(self, user_id):
        # create User instance from json data located in request body
        new_user = UserSchema().load(request.json)
        # test id mismatch
        if str(new_user.id) != user_id:
            abort(400, "id mismatch")
        # just creating the User instance, data is saved with commit
        db.session.commit()
        # return serialized user using 200 response code
        return UserSchema().dump(new_user)


@api_user.route("/")
class UserListController(Resource):
    @flask_praetorian.auth_required
    def get(self):
        # when returning several instances, UserSchema must receive: many=True
        # User.query.all(): list all users
        return UserSchema(many=True).dump(User.query.all())

    @flask_praetorian.auth_required
    @api_user.expect(UserSchema().get_model(api_user))
    @api_user.response(201, "Because I ordered it", UserSchema().get_model(api_user))
    def post(self):
        user = UserSchema().load(request.json)
        # hash_password
        guard = flask_praetorian.Praetorian()
        guard.init_app(current_app, User)
        user.hashed_password = guard.hash_password(user.hashed_password)

        # add new user
        db.session.add(user)
        db.session.commit()
        return UserSchema().dump(user), 201


@api_user.route("/roles")
class RolesListController(Resource):
    @flask_praetorian.auth_required
    def get(self):
        # using custom SQL. Similar to php's prepare statement
        statement = text("""
            select role.name, count(user.id) as members from user
                join roles_users ru on user.id = ru.user_id
                join role on ru.role_id = role.id
                group by role.name
            """)
        # execute statement
        result = db.session.execute(statement)
        # result is not serializable, we use a dictionary instead
        return jsonify({r['name']: r['members'] for r in result})
