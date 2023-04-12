from datetime import timedelta
import os


def init_cfg(app):
    # JWT config
    app.config["JWT_SECRET_KEY"] = "super-secret-key))"  # Change this!
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=30)
    app.config['JWT_TOKEN_LOCATION'] = ['cookies']
    # app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)

    # SQL Alchemy config
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///' + os.path.join(basedir, '../database/database.db')