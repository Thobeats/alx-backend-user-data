#!/usr/bin/env python3
"""Flask App"""
from flask import Flask, jsonify, Response, request, abort
from auth import Auth


app = Flask(__name__)
AUTH = Auth()


@app.route("/", methods=["GET"], strict_slashes=False)
def hello() -> Response:
    """GET /
    Return: welcome message
    """
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"], strict_slashes=False)
def users() -> tuple[Response, int]:
    """POST /users
    Register a user
    Return: user data
    """
    email = request.form.get("email")
    password = request.form.get("password")
    try:
        AUTH.register_user(email, password)
    except ValueError:
        return jsonify({"message": "email already registered"}), 400
    return jsonify({"email": email, "message": "user created"}), 200


@app.route("/sessions", methods=["POST"], strict_slashes=False)
def login() -> str:
    """POST /sessions
    Log in a user
    Return: session_id
    """
    email = request.form.get("email")
    password = request.form.get("password")
    if not AUTH.valid_login(email, password):
        abort(401)
    session_id = AUTH.create_session(email)
    if not session_id:
        abort(401)
    response = jsonify({"email": email, "message": "logged in"})
    return response.set_cookie(key="session_id", value=session_id)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
