import base64
import os
from datetime import datetime
from datetime import timezone

import flask
from flask_jwt_extended import create_access_token, verify_jwt_in_request, set_access_cookies, \
    unset_jwt_cookies
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import decode_token

from database.model.token import TokenBlocklist
from database.model.user import User
from database.db import db

import re


def login():
    # get username and password from request (form)
    username = flask.request.form.get('username', None)
    password = flask.request.form.get('password', None)
    if not username:
        return flask.jsonify({"msg": "Missing username parameter"}), 400
    if not password:
        return flask.jsonify({"msg": "Missing password parameter"}), 400

    user = User.query.filter_by(username=username).first()
    if user is None or user.password != password:
        return flask.jsonify({"msg": "Bad username or password"}), 401

    # blocklist all tokens from a user when he logs in
    token = user.access_token
    if token is not None and token:
        token = decode_token(token, csrf_value=None, allow_expired=True)
        jti = token['jti']
        ttype = token['type']
        now = datetime.now(timezone.utc)
        db.session.add(TokenBlocklist(jti=jti, type=ttype, created_at=now))
        db.session.commit()
        resp = flask.jsonify({'logout': True})
        unset_jwt_cookies(resp)

    access_token = create_access_token(identity=username)
    # refresh_token = create_refresh_token(identity=username)

    user.access_token = access_token
    # user.refresh_token = refresh_token
    db.session.commit()

    resp = flask.jsonify({'login': True})
    set_access_cookies(resp, access_token)

    return resp, 200


def login_form():
    return flask.render_template('login.html')

# @jwt_required(refresh=True)
# def refresh():
#     identity = get_jwt_identity()
#
#     user = User.query.filter_by(username=identity).first()
#
#     token = decode_token(user.access_token, csrf_value=None, allow_expired=True)
#     jti = token['jti']
#     ttype = token['type']
#     now = datetime.now(timezone.utc)
#     db.session.add(TokenBlocklist(jti=jti, type=ttype, created_at=now))
#     db.session.commit()
#
#     access_token = create_access_token(identity=identity)
#
#     user.access_token = access_token
#     db.session.commit()
#
#     return flask.jsonify(access_token=access_token)


@jwt_required()
def who_i_am():
    identity = get_jwt_identity()
    user = User.query.filter_by(username=identity).first()
    if user is None:
        return flask.jsonify({"msg": "Bad username or password"}), 401
    return flask.jsonify(id=user.id, username=user.username, admin=user.admin), 200


# logout route
@jwt_required()
def modify_token():
    identity = get_jwt_identity()

    user = User.query.filter_by(username=identity).first()
    token = user.access_token
    token = decode_token(token, csrf_value=None, allow_expired=True)
    jti = token["jti"]
    ttype = token["type"]
    now = datetime.now(timezone.utc)
    db.session.add(TokenBlocklist(jti=jti, type=ttype, created_at=now))
    db.session.commit()

    return flask.jsonify(msg=f"{ttype.capitalize()} token successfully revoked"), 200


@jwt_required()
def add_user():
    if not flask.request.is_json:
        return flask.jsonify({"msg": "Missing JSON in request"}), 400

    # check if current user is admin
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).first()
    if not user.admin:
        return flask.jsonify({"msg": "You are not admin("}), 403

    user = User()
    user.username = flask.request.json.get('username', None)
    user.password = flask.request.json.get('password', None)
    user.admin = flask.request.json.get('admin', None)
    if not user.username:
        return flask.jsonify({"msg": "Missing username parameter"}), 400
    if not user.password:
        return flask.jsonify({"msg": "Missing password parameter"}), 400
    if not user.admin:
        return flask.jsonify({"msg": "Missing admin parameter"}), 400

    # check if admin with this username already exists
    if User.query.filter_by(username=user.username).first():
        return flask.jsonify({"msg": "Admin with this username already exists"}), 409

    db.session.add(admin)
    db.session.commit()

    return flask.jsonify({"msg": "User added"}), 200


@jwt_required()
def delete_user():
    if not flask.request.is_json:
        return flask.jsonify({"msg": "Missing JSON in request"}), 400

    # check if current user is admin
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).first()
    if not user.admin:
        return flask.jsonify({"msg": "You are not admin("}), 403

    user_id = flask.request.json.get('user_id', None)

    if not user_id:
        return flask.jsonify({"msg": "Missing user_id parameter"}), 400

    user = User.query.filter_by(id=user_id).first()

    # check if admin with this id exists
    if not user:
        return flask.jsonify({"msg": "User with this id does not exists"}), 404

    db.session.delete(admin)
    db.session.commit()
    return flask.jsonify({"msg": "User deleted"}), 200


@jwt_required()
def get_users():
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).first()
    if not user.admin:
        return flask.jsonify({"msg": "You are not admin("}), 403

    users = User.query.all()
    return flask.jsonify([user.serialize() for user in users]), 200


def get_identity_if_logedin():
    try:
        verify_jwt_in_request()
        return get_jwt_identity()
    except Exception:
        pass
    return None


def index():
    identity = get_identity_if_logedin()
    if not identity:
        return flask.render_template('index.html', user="None")
    user = User.query.filter_by(username=identity).first()
    return flask.render_template('index.html', user=user.username)


def init_routes(app):
    app.add_url_rule('/login', 'login', login, methods=['POST'])
    app.add_url_rule('/login', 'login_form', login_form, methods=['GET'])
    # app.add_url_rule('/refresh', 'refresh', refresh, methods=['POST'])
    app.add_url_rule('/who_i_am', 'who_i_am', who_i_am, methods=['GET'])
    app.add_url_rule('/logout', 'logout', modify_token, methods=['DELETE'])
    app.add_url_rule('/add_user', 'add_user', add_user, methods=['POST'])
    app.add_url_rule('/delete_user', 'delete_user', delete_user, methods=['POST'])
    app.add_url_rule('/get_users', 'get_users', get_users, methods=['GET'])
    app.add_url_rule('/', 'index', index, methods=['GET'])
