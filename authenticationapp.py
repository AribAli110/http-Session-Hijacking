from flask import Flask, request, render_template, redirect, url_for, make_response
import hashlib
import os

app = Flask(__name__)

# Simulated user database
USER_DB = {
    "admin": hashlib.sha256("password123".encode()).hexdigest()  # Username: admin, Password: password123
}

# Simulated session storage
SESSIONS = {}

@app.route('/')
def home():
    session_id = request.cookies.get('session_id')
    if session_id in SESSIONS:
        username = SESSIONS[session_id]
        return render_template('welcome.html', username=username)
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = hashlib.sha256(request.form['password'].encode()).hexdigest()

        if username in USER_DB and USER_DB[username] == password:
            session_id = os.urandom(16).hex()
            SESSIONS[session_id] = username
            response = make_response(redirect(url_for('home')))
            response.set_cookie('session_id', session_id)
            return response
        else:
            return "<h1>Invalid Credentials</h1><a href='/login'>Try Again</a>", 401

    return render_template('login.html')

@app.route('/logout')
def logout():
    session_id = request.cookies.get('session_id')
    if session_id in SESSIONS:
        del SESSIONS[session_id]
    response = make_response(redirect(url_for('login')))
    response.set_cookie('session_id', '', expires=0)
    return response

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
