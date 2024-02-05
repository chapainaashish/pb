#this python file will make the website folder an python package

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager


# SQLAlchemy instance initialization. This object will be used for all the SQLAlchemy operations.
db = SQLAlchemy()
DB_NAME = "database.db"

# Function to create and configure the Flask application.
def create_app():
    # Creating an instance of the Flask class. This instance represents your web application.
    app = Flask(__name__, static_folder='static')
    # Setting the secret key for the Flask application. This key should be a random and secure token.
    app.config['SECRET_KEY'] = 'tempCODE123'
    # Configuring the database URI for SQLAlchemy. This tells SQLAlchemy which database to connect to.
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    # Initializing the SQLAlchemy instance with the Flask app.
    db.init_app(app)

    from .views import views
    from .auth import auth

    # Registering blueprints. Blueprints are used for organizing your application into distinct components.
    app.register_blueprint(views, url_prefix= '/')
    app.register_blueprint(auth, url_prefix= '/')

    from .models import User, Image
    
    # Creating the database tables based on the models.
    with app.app_context():
        db.create_all()
        print('Database ready to use')

    # Initializing the LoginManager. This is used for managing user sessions in Flask.
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    # User loader callback for Flask-Login. It loads a user from the database by ID.
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    # Returning the Flask app instance.
    return app

