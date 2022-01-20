from flask import Flask
from users import blueprint as api_user
from owners import blueprint as api_owner
from pets import blueprint as api_pet
from model import init_db

app = Flask(__name__)
init_db(app)
# register blueprints
app.register_blueprint(api_user, url_prefix="/api/user/")
app.register_blueprint(api_owner, url_prefix="/api/owner/")
app.register_blueprint(api_pet, url_prefix="/api/pet/")


# link to api to avoid 404 on /
@app.route("/")
def home():
    return app.send_static_file("index.html")


if __name__ == '__main__':
    app.run(debug=True)
