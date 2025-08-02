# app.py — complete Flask app for your assignment

import sqlite3
import json
from flask import Flask, request, jsonify, abort

from services.user_service import (
    fetch_all_users,
    fetch_user_by_id,
    search_users_by_name,
)
from services.auth_service import verify_user_login

app = Flask(__name__)

@app.route("/")
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

@app.route("/search")
def search():
    name = request.args.get("name", "").strip()
    results = search_users_by_name(name)
    return jsonify(results), 200

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json(force=True) or {}
    username = data.get("username") or data.get("email")
    password = data.get("password")
    if not username or not password:
        abort(400)
    if verify_user_login(username, password):
        return jsonify({"status": "success"}), 200
    return jsonify({"status": "invalid credentials"}), 401

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
