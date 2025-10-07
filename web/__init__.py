import os

from flask import Flask
from flask_wtf.csrf import CSRFProtect

csrf = CSRFProtect()

def create_app(test_config=None):
    # create and configure the app
    app = Flask(import_name=__name__, instance_relative_config=True)
    app.secret_key = os.environ.get('SECRET_KEY', default=os.urandom(24))


    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile(filename='config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(mapping=test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(name=app.instance_path)
    except OSError:
        pass

    from .views import auth, dashboard, clients, contracts, work_orders, activity_reports, invoices
    app.register_blueprint(blueprint=auth.bp)
    app.register_blueprint(blueprint=dashboard.bp)
    app.register_blueprint(blueprint=clients.bp)
    app.register_blueprint(blueprint=contracts.bp)
    app.register_blueprint(blueprint=work_orders.bp)
    app.register_blueprint(blueprint=activity_reports.bp)
    app.register_blueprint(blueprint=invoices.bp)

    # a simple page that says hello
    @app.route(rule='/health')
    def health_check():
        return 'healthy'

    csrf.init_app(app=app)

    return app