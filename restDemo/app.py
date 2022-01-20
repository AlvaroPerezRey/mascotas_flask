from flask import Flask, jsonify, request
import flask_praetorian
from model import init_db, User

# import blueprints
from views.users import blueprint as api_user
from views.owners import blueprint as api_owner
from views.pets import blueprint as api_pet

guard = flask_praetorian.Praetorian()
# TODO: cors config

app = Flask(__name__)
app.config["SECRET_KEY"] = "latch"
app.config["JWT_ACCESS_LIFESPAN"] = {"hours": 24}
app.config["JWT_REFRESH_LIFESPAN"] = {"days": 30}
guard.init_app(app, User)
init_db(app, guard)

# register blueprints
app.register_blueprint(api_user, url_prefix="/api/user/")
app.register_blueprint(api_owner, url_prefix="/api/owner/")
app.register_blueprint(api_pet, url_prefix="/api/pet/")


# link to api to avoid 404 on /
@app.route("/")
def home():
    return app.send_static_file("index.html")


# authentication system
@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    user = guard.authenticate(username, password)
    ret = {"access_token": guard.encode_jwt_token(user)}
    return jsonify(ret), 200


if __name__ == '__main__':
    app.run(debug=True)
