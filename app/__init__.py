from config import Config
from copy import deepcopy
from flask import Flask
from flask_admin import Admin
from flask_apscheduler import APScheduler
from flask_blogging_patron import BloggingEngine, SQLAStorage
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_principal import Permission, RoleNeed
from flask_sqlalchemy import SQLAlchemy


# extensions
bootstrap = Bootstrap()
db = SQLAlchemy()
migrate = Migrate()
global sql_storage
blog_engine = BloggingEngine()
login = LoginManager()
login.login_view = 'auth.login'
login.login_message_category = 'info'
mail = Mail()
scheduler = APScheduler()
admin = Admin(name='LibrePatron Admin', template_mode='bootstrap3')

# global
global temp_bp

# permissions - flask_principal objects created by BloggingEngine
principals = blog_engine.principal
admin_permission = Permission(RoleNeed('admin'))


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    bootstrap.init_app(app)
    db.init_app(app)
    with app.app_context():
        global sql_storage
        sql_storage = SQLAStorage(db=db)
    migrate.init_app(app, db)
    login.init_app(app)
    mail.init_app(app)
    admin.init_app(app)
    blog_engine.init_app(app, sql_storage)
    scheduler.init_app(app)
    scheduler.start()

    # deepcopy auto-generated flask_blogging bp, then delete it
    global temp_bp
    temp_bp = deepcopy(app.blueprints['blogging'])
    del app.blueprints['blogging']

    # blueprints
    from app.api import bp as api_bp
    from app.auth import bp as auth_bp
    from app.blogging import bp as blogging_bp
    from app.main import bp as main_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(
        blogging_bp,
        url_prefix=app.config.get('BLOGGING_URL_PREFIX')
    )
    app.register_blueprint(main_bp)

    # tasks
    from app import tasks

    return app


from app import admin_views
from app import models, subscriptions
