import json
import sqlite3
from flask import Flask, request, jsonify, abort
from services.auth_service import verify_user_login
from services.user_service import (
    fetch_all_users,
    fetch_user_by_id,
    search_users_by_name,
)

app = Flask(__name__)  # Must come before any @app.route declarations

@app.route("/", methods=["GET"])
def health():
    return "OK", 200

@app.route("/users", methods=["GET"])
def list_users():
    return jsonify(fetch_all_users()), 200

@app.route("/user/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = fetch_user_by_id(user_id)
    if not user:
        abort(404)
    return jsonify(user), 200

@app.route("/search", methods=["GET"])
def search():
    name = request.args.get("name", "")
    return jsonify(search_users_by_name(name)), 200

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json(force=True) or {}
    login_key = data.get("username") or data.get("email")
    password = data.get("password")
    if not login_key or not password:
        abort(400)
    if verify_user_login(login_key, password):
        return jsonify({"status": "success"}), 200
    return jsonify({"status": "invalid credentials"}), 401

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
