import streamlit as st
from flask import Flask, jsonify, redirect, url_for, render_template, request
import jwt
import datetime
from blueprints.chart.chart_app import chart_appbp

def init_connection():
    return psycopg2.connect(**st.secrets["postgres"])

app = Flask(__name__)
app.register_blueprint(chart_appbp, url_prefix='/chart')

secret_key = "sadfksxdcfvgbn./'.;,lmgfl"  # Replace with your actual secret key

# Example users (in a real application, fetch users from the database)
example_users = [
    {"username": "santhosh", "password": "sandi"},
    {"username": "santhosh22", "password": "sandi"}
]

# Protected route requiring authentication
@app.route('/protected')
def protected():
    token = request.cookies.get('jwt_token')

    if token:
        try:
            # Verify the token
            payload = jwt.decode(token, secret_key, algorithms=['HS256'])
            username = payload.get('username')
            return f"Welcome, {username}! This is a protected route."
        except jwt.ExpiredSignatureError:
            return "Token has expired. Please log in again."
        except jwt.InvalidTokenError:
            return "Invalid token. Please log in again."
    else:
        return redirect(url_for('index'))

@app.route('/chart/')
def chart():
    return render_template('chart.html')
    
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    data = request.form

    # Assuming the user enters username and password in the form
    username = data.get('username')
    entered_password = data.get('password')

    # Validate the username and password
    if any(user["username"] == username and user["password"] == entered_password for user in example_users):
        # Generate JWT token
        token = generate_jwt_token(username)

        # Set the JWT token in a cookie
        response = jsonify({'token': token})
        response.set_cookie('jwt_token', token, httponly=True, secure=True)  # Secure flag for HTTPS
        return response
    else:
        # Hint for an invalid password
        return jsonify({'message': 'Invalid password. Please check your password and try again.'}), 401

def generate_jwt_token(username):
    payload = {
        'username': username,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)  # Set the expiration time
    }
    token = jwt.encode(payload, secret_key, algorithm='HS256')
    return token

if __name__ == '__main__':
    app.run(debug=True)
