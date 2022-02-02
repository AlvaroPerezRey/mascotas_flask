import os

class Config:
    ###
    # database configuration
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.abspath(os.curdir)}/flask.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    ###
    # praetorian configuration
    SECRET_KEY = "latch"
    JWT_ACCESS_LIFESPAN = {"hours": 24}
    JWT_REFRESH_LIFESPAN = {"days": 30}

    ###
    # gitHub OAuth config
    GITHUB_CLIENT_ID = "de3719ce10145f958512"
    GITHUB_CLIENT_SECRET = "ebb4e8244e0fbb4a47f4c4e519d39bbeb8e3b3b0"

    ###
    # using environment variables
    # import os
    # GITHUB_CLIENT_ID = os.getenv("GITHUB_CLIENT_ID")
    # GITHUB_CLIENT_SECRET = os.getenv("GITHUB_CLIENT_SECRET")

class ConfigTesting(Config):
    """
    App configuration
    """

    ###
    # database configuration
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

    # En teoría todo lo común está aquí por herencia, pero alguna vez
    # ha fallado, no sé por qué.

### Así está en el blog:

# basedir = os.path.abspath(os.path.dirname(__file__))
# class Config(object):
#     SECRET_KEY = '736670cb10a600b695a55839ca3a5aa54a7d7356cdef815d2ad6e19a2031182b'
#     RECAPTCHA_PUBLIC_KEY = "6LdKkQQTAAAAAEH0GFj7NLg5tGicaoOus7G9Q5Uw"
#     RECAPTCHA_PRIVATE_KEY = '6LdKkQQTAAAAAMYroksPTJ7pWhobYb88fTAcxcYn'
#     POSTS_PER_PAGE = 10

#     TWITTER_API_KEY = "XXXX"
#     TWITTER_API_SECRET = "XXXX"
#     FACEBOOK_CLIENT_ID = "XXX"
#     FACEBOOK_CLIENT_SECRET = "XXXX"
    
# class ProdConfig(Config):
#     SQLALCHEMY_TRACK_MODIFICATIONS = False
#     #SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data.db')
#     SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'database.db')


# class DevConfig(Config):
#     DEBUG = True
#     #SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(os.path.dirname(__file__), '..', 'data.db')
#     #SQLALCHEMY_DATABASE_URI = 'sqlite:///data.db'
#     SQLALCHEMY_TRACK_MODIFICATIONS = True #False
#     SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'database.db')
#     #print(SQLALCHEMY_DATABASE_URI)
#     #SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@localhost:3306/flask_blog'
#     #SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:root@localhost:3306/flask_blog'
#     SQLALCHEMY_ECHO = True # para ver las consultas que se hacen a la base de datos para




### Luego en la creación de la app, importar la clase Config o  ConfigTesting y se la pasas a la app.    
### Alternativamente puedes tener esto en la app:

# import os
# from webapp import create_app

## 'WEBAPP_ENV' es una variable de entorno que se puede usar para decir que config hay que usar
# env = os.environ.get('WEBAPP_ENV', 'dev') # dev, test, prod o las configuraciones que tengas
# app = create_app('config.%sConfig' % env.capitalize())


# if __name__ == '__main__':
#     app.run()

### Y en el __init__.py de "webapp" la función create_app:

# from flask import Flask

# from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate

# db = SQLAlchemy()
# migrate = Migrate()


# def create_app(object_name):
#     """
#     An flask application factory, as explained here:
#     http://flask.pocoo.org/docs/patterns/appfactories/

#     Arguments:
#         object_name: the python path of the config object,
#                      e.g. project.config.ProdConfig
#     """
#     app = Flask(__name__)
#     app.config.from_object(object_name)

#     db.init_app(app)
#     migrate.init_app(app, db)

    ## las distinntas partes de la app separadas por carpetas 
#     from .auth import create_module as auth_create_module
#     from .blog import create_module as blog_create_module
#     from .main import create_module as main_create_module
#     from .api import create_module as api_create_module
#     auth_create_module(app)
#     blog_create_module(app)
#     main_create_module(app)
#     api_create_module(app)

#     return app

