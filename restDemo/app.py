from flask import Flask, jsonify, request
from authlib.integrations.flask_client import OAuth
import flask_praetorian

from model import init_db, User

# import blueprints
from views.users import blueprint as api_user
from views.owners import blueprint as api_owner
from views.pets import blueprint as api_pet

# instantiate praetorian object
guard = flask_praetorian.Praetorian()
# TODO: cors config

app = Flask(__name__)

# instantiate oauth object
oauth = OAuth(app)
# oauth init
oauth.register(
    name='github',
    client_id='de3719ce10145f958512',
    client_secret='ebb4e8244e0fbb4a47f4c4e519d39bbeb8e3b3b0',
    access_token_url='https://github.com/login/oauth/access_token',
    access_token_params=None,
    authorize_url='https://github.com/login/oauth/authorize',
    authorize_params=None,
    api_base_url='https://api.github.com/',
    client_kwargs={'scope': 'user:email'},
)


# praetorian config
app.config["SECRET_KEY"] = "latch"
app.config["JWT_ACCESS_LIFESPAN"] = {"hours": 24}
app.config["JWT_REFRESH_LIFESPAN"] = {"days": 30}
# praetorian init
guard.init_app(app, User)

# SQLAlchemy init
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
    # get username and password from body (json)
    username = request.json.get('username')
    password = request.json.get('password')
    # praetorian authentication
    user = guard.authenticate(username, password)
    # get JWT from praetorian
    ret = {"access_token": guard.encode_jwt_token(user)}
    # return JWT
    return jsonify(ret), 200


@app.route('/github')
def oauth_login():
    github = oauth.create_client('github')
    redirect_uri = 'http://localhost:5000/authorize'
    return github.authorize_redirect(redirect_uri)


@app.route('/authorize')
def authorize():
    token = oauth.github.authorize_access_token()
    resp = oauth.github.get('user', token=token)
    resp.raise_for_status()
    profile = resp.json()
    return jsonify([token, profile])


if __name__ == '__main__':
    app.run(debug=True)
