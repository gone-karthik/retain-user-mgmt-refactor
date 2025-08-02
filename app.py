@app.route("/login", methods=["POST"])
def login():
-    data = json.loads(request.get_data())
-    email = data["email"]
+    data = request.get_json(force=True) or {}
+    username = data.get("username") or data.get("email")
     password = data.get("password")

-    if not email or not password:
-        abort(400)
-    ok = verify_user_login(email, password)
+    if not username or not password:
+        abort(400)
+    ok = verify_user_login(username, password)

     if ok:
         return jsonify({"status": "success"}), 200

     return jsonify({"status": "invalid credentials"}), 401
