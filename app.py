import os
import time
from functools import wraps
from flask import Flask, request, jsonify, Response

app = Flask(__name__)

USERS = {}

def load_users_from_file(filepath="users.txt"):
    """
    Loads users and passwords from a file into the USERS dictionary.
    The file should have one 'username:password' pair per line.
    """
    global USERS
    try:
        with open(filepath, 'r') as f:
            for line in f:
                line = line.strip()
                if not line or ':' not in line:
                    continue
                # Split only on the first colon to allow colons in passwords
                username, password = line.split(':', 1)
                USERS[username.strip()] = password.strip()
        if not USERS:
            print("Warning: users.txt is empty or improperly formatted. No users were loaded.")
            exit(1)
    except FileNotFoundError:
        print(f"Warning: User credentials file not found at '{filepath}'. Authentication will fail.")
        exit(1)
    except Exception as e:
        print(f"An error occurred while loading users: {e}")
        exit(1)

# Load users on application startup
load_users_from_file()


# --- Environment Variable for Readiness ---
try:
    # Default readiness time is 30 seconds
    readiness_time = int(os.environ.get('READINESS_TIME', '30'))
except ValueError:
    readiness_time = 30

# Record the time when the application starts
start_time = time.time()


# --- Authentication Helper Functions ---

def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid."""
    return username in USERS and USERS[username] == password

def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
        'Could not verify your access level for that URL.\n'
        'You have to login with proper credentials', 401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'})

def auth_required(f):
    """Decorator to protect endpoints with authentication."""
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

try:
    readiness_time = int(os.environ.get('READINESS_TIME', '30'))
except ValueError:
    readiness_time = 30

# Record the time when the application starts
start_time = time.time()


@app.route("/")
@auth_required
def get_ip():
    if request.headers.getlist("X-Forwarded-For"):
        ip = request.headers.getlist("X-Forwarded-For")[0].split(',')[0]
    else:
        ip = request.remote_addr
    return jsonify(ip=ip)


@app.route("/health")
def health_check():
    if time.time() - start_time >= readiness_time:
        return jsonify(status="healthy")
    else:

        return jsonify(status="not_ready"), 200


@app.route("/ready")
def readiness_probe():
    if time.time() - start_time >= readiness_time:
        return jsonify(status="ready"), 200
    else:

        return jsonify(status="not_ready"), 503


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
