from flask import Blueprint, request
from flask_restx import abort, Api, Resource
from model import Owner, db, OwnerSchema


blueprint = Blueprint('owners', __name__)
api_owner = Api(blueprint, doc="/docs")


@api_owner.route("/<owner_id>")
class OwnerController(Resource):
    def get(self, owner_id):
        owner = Owner.query.get_or_404(owner_id)
        return OwnerSchema().dump(owner)

    def delete(self, owner_id):
        owner = Owner.query.get_or_404(owner_id)
        db.session.delete(owner)
        db.session.commit()
        return f"Deleted owner {owner_id}", 204

    def put(self, owner_id):
        new_owner = OwnerSchema().load(request.json)
        if str(new_owner.id) != owner_id:
            abort(400, "id mismatch")
        db.session.commit()
        return OwnerSchema().dump(new_owner)


@api_owner.route("/")
class OwnerListController(Resource):
    def get(self):
        return OwnerSchema(many=True).dump(Owner.query.all())

    def post(self):
        owner = OwnerSchema().load(request.json)
        db.session.add(owner)
        db.session.commit()
        return OwnerSchema().dump(owner), 201
