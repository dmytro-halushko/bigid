import os
import time
from flask import Flask, request, jsonify

app = Flask(__name__)

try:
    readiness_time = int(os.environ.get('READINESS_TIME', '30'))
except ValueError:
    readiness_time = 30

# Record the time when the application starts
start_time = time.time()


@app.route("/")
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

        return jsonify(status="not_ready"), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
