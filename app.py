import json
from flask import Flask, request, jsonify, abort
from services.auth_service import verify_user_login
from services.user_service import (
    health_check,
    fetch_all_users,
    fetch_user,
    search_users,
    create_user,
    update_user,
    delete_user,
)

app = Flask(__name__)

@app.route("/", methods=["GET"])
def health():
    return health_check()

@app.route("/users", methods=["GET"])
def list_users():
    users = fetch_all_users()
    return jsonify(users), 200

@app.route("/user/<user_id>", methods=["GET"])
def get_user(user_id):
    user = fetch_user(user_id)
    if not user:
        abort(404, description=f"User {user_id} not found")
    return jsonify(user), 200

@app.route("/users", methods=["POST"])
def create_new_user():
    try:
        body = request.get_json(force=True)
    except (json.JSONDecodeError, TypeError):
        abort(400, description="Invalid JSON")
    try:
        new_user = create_user(body)
    except ValueError as e:
        abort(400, description=str(e))
    return jsonify(new_user), 201

@app.route("/user/<user_id>", methods=["PUT"])
def update_existing_user(user_id):
    try:
        body = request.get_json(force=True)
    except (json.JSONDecodeError, TypeError):
        abort(400, description="Invalid JSON")
    try:
        updated = update_user(user_id, body)
    except ValueError as e:
        abort(400, description=str(e))
    if not updated:
        abort(404, description=f"User {user_id} not found")
    return jsonify(updated), 200

@app.route("/user/<user_id>", methods=["DELETE"])
def delete_existing_user(user_id):
    deleted = delete_user(user_id)
    if not deleted:
        abort(404, description=f"User {user_id} not found")
    return "", 204

@app.route("/search", methods=["GET"])
def search_by_name():
    name = request.args.get("name")
    if not name:
        abort(400, description="name param is required")
    results = search_users(name)
    return jsonify(results), 200

@app.route("/login", methods=["POST"])
def login():
    try:
        body = request.get_json(force=True) or {}
    except (json.JSONDecodeError, TypeError):
        abort(400, description="Invalid JSON")
    login_key = body.get("username") or body.get("email")
    password = body.get("password")

    if not login_key or not password:
        abort(400, description="username/email and password required")

    if verify_user_login(login_key, password):
        return jsonify({"status": "success"}), 200
    else:
        return jsonify({"status": "unauthorized"}), 401

# Ensure the app object is exposed for pytest / flask dev server
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
