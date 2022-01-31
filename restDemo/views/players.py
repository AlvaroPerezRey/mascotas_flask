import flask_praetorian
from flask import request
from flask_restx import abort, Resource, Namespace

from model import Player, db, PlayerSchema

# namespace declaration
api_player = Namespace("Players", "Players management")


@api_player.route("/<player_id>")
class PlayerController(Resource):
    # methods for http methods supported
    # auth required
    @flask_praetorian.auth_required
    def get(self, player_id):
        # gets one player by id
        player = Player.query.get_or_404(player_id)
        # PlayerSchema() is an object used for ORM objects serialization
        return PlayerSchema().dump(player)

    # roles required (if several roles, player must have every role)
    @flask_praetorian.roles_required("admin")
    def delete(self, player_id):
        player = Player.query.get_or_404(player_id)
        # delete player
        db.session.delete(player)
        # commit needed after every writing operation (not query)
        db.session.commit()
        # using 204 response code
        return f"Deleted player {player_id}", 204

    @flask_praetorian.roles_required("admin")
    def put(self, player_id):
        # create Player instance from json data located in request body
        new_player = PlayerSchema().load(request.json)
        # test id mismatch
        if str(new_player.id) != player_id:
            abort(400, "id mismatch")
        # just creating the Player instance, data is saved with commit
        db.session.commit()
        # return serialized player using 200 response code
        return PlayerSchema().dump(new_player)


@api_player.route("/")
class PlayerListController(Resource):
    @flask_praetorian.auth_required
    def get(self):
        # when returning several instances, PlayerSchema must receive: many=True
        # Player.query.all(): list all players
        return PlayerSchema(many=True).dump(Player.query.all())

    @flask_praetorian.roles_required("admin")
    def post(self):
        player = PlayerSchema().load(request.json)
        # add new player
        db.session.add(player)
        db.session.commit()
        return PlayerSchema().dump(player), 201
