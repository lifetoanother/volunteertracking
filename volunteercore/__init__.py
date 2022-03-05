import os
from flask import Flask, render_template, redirect, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user, login_required
from flask_migrate import Migrate
from config import Config
import flask_whooshalchemyplus

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'login.html'

def create_app(config_class=Config):
    app = Flask(__name__)
    app.template_folder = './pages'
    app.config.from_object(config_class)
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    flask_whooshalchemyplus.init_app(app)

    # Register blueprints
    from volunteercore.auth import bp as auth_bp
    app.register_blueprint(auth_bp)
    from volunteercore.volops import bp as volops_bp
    app.register_blueprint(volops_bp)
    from volunteercore.api import bp as api_bp
    app.register_blueprint(api_bp)
    from volunteercore.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    @app.route('/')
    @app.route('/index')
    @app.route('/index.html')
    def index():
        if session.get('user_id') == None:
            return redirect('login.html')
        return render_template('index.html')
    
    @app.route('/login')
    @app.route('/login.html')
    def login():
        if current_user.is_authenticated:
            return redirect('index.html')
        return render_template('login.html')

    return app
