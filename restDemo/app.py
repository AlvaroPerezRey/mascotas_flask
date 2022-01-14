from flask import Flask, send_from_directory
from users import blueprint as api_user
from model import init_db

app = Flask(__name__)
init_db(app)
app.register_blueprint(api_user, url_prefix="/api/user/")

@app.route("/")
def home():
    return app.send_static_file("index.html")

if __name__ == '__main__':
    app.run(debug=True)
