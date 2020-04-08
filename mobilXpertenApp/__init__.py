import os, logging
from logging.handlers import SMTPHandler, RotatingFileHandler
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from config import Config

login = LoginManager()
mail = Mail()
db = SQLAlchemy()
migrate = Migrate()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    mail.init_app(app)
   # app.elasticsearch = Elasticsearch([app.config['ELASTICSEARCH_URL']]) \
       # if app.config['ELASTICSEARCH_URL'] else None
   #app.redis = Redis.from_url(app.config['REDIS_URL'])
   # app.task_queue = rq.Queue('microblog-tasks', connection=app.redis)

    #from mobilXpertenApp.errors import bp as errors_bp
    #app.register_blueprint(errors_bp)

    from mobilXpertenApp.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    from mobilXpertenApp.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    if not app.debug:
        if app.config['MAIL_SERVER']:
            auth = None
        if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
            auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
        secure = None
        if app.config['MAIL_USE_TLS']:
            secure = ()
        mail_handler = SMTPHandler(
            mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
            fromaddr='no-reply@' + app.config['MAIL_SERVER'],
            toaddrs=app.config['ADMINS'], subject='MobilXperten Failure',
            credentials=auth, secure=secure)
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/mobilXperten.log', maxBytes=10240,
                                        backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))


    return app


from mobilXpertenApp import routes, models
