import flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS

from resources import config
from resources.routes import init_routes
from database.db import create_db

# create flask app
app = flask.Flask(__name__)

# init app
config.init_cfg(app)

# init routes
init_routes(app)

# init jwt
jwt = JWTManager(app)

# init cors
CORS(app)
cors = CORS(app, resource={
    r"/*": {
        "origins": "*"
    }
})


# init db
@app.before_first_request
def create_tables():
    create_db(app, jwt)


# run app
if __name__ == '__main__':
    app.run("0.0.0.0", 5000, debug=True)
