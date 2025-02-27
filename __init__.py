from flask import Flask
import secrets
from datetime import timedelta

def create_app():
    app = Flask('__name__')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = secrets.token_hex(16)
    app.secret_key = secrets.token_hex(16)
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=30)
    app.permanent_session_lifetime = timedelta(days=30)

    from app.routes import api, auth, scoring, user, dashboard, recommandation
    from app.routes.dashboard import create_dashboard

    app.register_blueprint(api, url_prefix='/api')
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(scoring, url_prefix='/scoring')
    app.register_blueprint(recommandation, url_prefix='/recommandation')
    app.register_blueprint(user, url_prefix='/user')
    app.register_blueprint(dashboard, url_prefix='/dashboard')

    

    create_dashboard(app)

    return app