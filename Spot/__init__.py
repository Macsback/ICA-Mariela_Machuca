from flask import Flask
from .mydb import db
from .routes import register_routes

def create_app():
    app = Flask(__name__)
    app.secret_key = "spot_secret_key"
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/spot_db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

 
    db.init_app(app)


    register_routes(app)

    return app

