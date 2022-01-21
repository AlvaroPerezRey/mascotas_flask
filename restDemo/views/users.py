from flask import Blueprint, request
import flask_praetorian
from flask_restx import abort, Api, Resource
from model import User, db, UserSchema


blueprint = Blueprint('users', __name__)
api_user = Api(blueprint, doc="/docs")
flask_praetorian.PraetorianError.register_error_handler_with_flask_restx(api_user)

@api_user.route("/<user_id>")
class UserController(Resource):
    @flask_praetorian.auth_required
    def get(self, user_id):
        user = User.query.get_or_404(user_id)
        return UserSchema().dump(user)

    @flask_praetorian.roles_required("admin")
    def delete(self, user_id):
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return f"Deleted user {user_id}", 204

    @flask_praetorian.roles_required("admin")
    def put(self, user_id):
        new_user = UserSchema().load(request.json)
        if str(new_user.id) != user_id:
            abort(400, "id mismatch")
        db.session.commit()
        return UserSchema().dump(new_user)


@api_user.route("/")
class UserListController(Resource):
    @flask_praetorian.auth_required
    def get(self):
        return UserSchema(many=True).dump(User.query.all())

    @flask_praetorian.roles_required("admin")
    def post(self):
        user = UserSchema().load(request.json)
        db.session.add(user)
        db.session.commit()
        return UserSchema().dump(user), 201
