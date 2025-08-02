import sqlite3
import json
from flask import Flask, request, jsonify, abort

from services.auth_service import verify_user_login

conn = sqlite3.connect('users.db', check_same_thread=False)
cursor = conn.cursor()

@app.route('/')
def home():
    return "User Management System"

@app.route('/users', methods=['GET'])
def get_all_users():
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    return str(users)

@app.route('/user/<user_id>', methods=['GET'])
def get_user(user_id):
    query = f"SELECT * FROM users WHERE id = '{user_id}'"
    cursor.execute(query)
    user = cursor.fetchone()
    
    if user:
        return str(user)
    else:
        return "User not found"

@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_data()
    data = json.loads(data)
    
    name = data['name']
    email = data['email']
    password = data['password']
    
    cursor.execute(f"INSERT INTO users (name, email, password) VALUES ('{name}', '{email}', '{password}')")
    conn.commit()
    
    print("User created successfully!")
    return "User created"

@app.route('/user/<user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_data()
    data = json.loads(data)
    
    name = data.get('name')
    email = data.get('email')
    
    if name and email:
        cursor.execute(f"UPDATE users SET name = '{name}', email = '{email}' WHERE id = '{user_id}'")
        conn.commit()
        return "User updated"
    else:
        return "Invalid data"

@app.route('/user/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    cursor.execute(f"DELETE FROM users WHERE id = '{user_id}'")
    conn.commit()
    
    print(f"User {user_id} deleted")
    return "User deleted"

@app.route('/search', methods=['GET'])
def search_users():
    name = request.args.get('name')
    
    if not name:
        return "Please provide a name to search"
    
    cursor.execute(f"SELECT * FROM users WHERE name LIKE '%{name}%'")
    users = cursor.fetchall()
    return str(users)

@app.route("/login", methods=["POST"])
def login():
    # Use force=True to parse JSON even if Content-Type isn't strictly application/json
    data = request.get_json(force=True) or {}

    # Accept either "username" or fall back to "email"
    username = data.get("username") or data.get("email")
    password = data.get("password")

    # Required fields check
    if not username or not password:
        abort(400)

    # Delegate the login check to our service function
    ok = verify_user_login(username, password)

    if ok:
        return jsonify({"status": "success"}), 200
    return jsonify({"status": "invalid credentials"}), 401
