from flask import Flask, request, render_template_string
import sqlite3
import hashlib
from Crypto.Cipher import AES
import base64

app = Flask(__name__)


# 🔐 AES ENCRYPTION SETUP

KEY = hashlib.sha256(b'mysecretkey').digest()

def pad(data):
    return data + b" " * (16 - len(data) % 16)

def encrypt(text):
    cipher = AES.new(KEY, AES.MODE_ECB)
    encrypted = cipher.encrypt(pad(text.encode()))
    return base64.b64encode(encrypted).decode()


# 🗄 DATABASE SETUP

def init_db():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            password TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()


# 🎨 HTML TEMPLATE (MERGED)

HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Secure App</title>
    <style>
        body {
            font-family: Arial;
            background: #f4f4f4;
            text-align: center;
            margin-top: 80px;
        }
        form {
            background: white;
            padding: 20px;
            display: inline-block;
            border-radius: 10px;
            box-shadow: 0px 0px 10px gray;
        }
        input {
            padding: 10px;
            margin: 10px;
            width: 200px;
        }
        button {
            padding: 10px 20px;
            background: #28a745;
            color: white;
            border: none;
            cursor: pointer;
        }
        button:hover {
            background: #218838;
        }
        .msg {
            color: green;
            margin-top: 10px;
        }
    </style>
</head>
<body>

    <h2>🔐 Secure Registration System</h2>

    <form method="POST">
        <input type="text" name="username" placeholder="Enter Username" required><br>
        <input type="password" name="password" placeholder="Enter Password" required><br>
        <button type="submit">Register</button>
    </form>

    <div class="msg">{{ message }}</div>

</body>
</html>
"""


# 🚀 ROUTES

@app.route("/", methods=["GET", "POST"])
def home():
    message = ""

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        encrypted_password = encrypt(password)

        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, encrypted_password)
        )
        conn.commit()
        conn.close()

        message = "✅ User registered securely!"

    return render_template_string(HTML_PAGE, message=message)


# ▶ RUN APP

if __name__ == "__main__":
    app.run(debug=True)
