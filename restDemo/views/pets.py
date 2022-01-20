from flask import Blueprint, request
from flask_restx import abort, Api, Resource
from model import Pet, db, PetSchema


blueprint = Blueprint('pets', __name__)
api_pet = Api(blueprint, doc="/docs")


@api_pet.route("/<pet_id>")
class PetController(Resource):
    def get(self, pet_id):
        pet = Pet.query.get_or_404(pet_id)
        return PetSchema().dump(pet)

    def delete(self, pet_id):
        pet = Pet.query.get_or_404(pet_id)
        db.session.delete(pet)
        db.session.commit()
        return f"Deleted pet {pet_id}", 204

    def put(self, pet_id):
        new_pet = PetSchema().load(request.json)
        if str(new_pet.id) != pet_id:
            abort(400, "id mismatch")
        db.session.commit()
        return PetSchema().dump(new_pet)


@api_pet.route("/")
class PetListController(Resource):
    def get(self):
        return PetSchema(many=True).dump(Pet.query.all())

    def post(self):
        pet = PetSchema().load(request.json)
        db.session.add(pet)
        db.session.commit()
        return PetSchema().dump(pet), 201
