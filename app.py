from flask import Flask, jsonify
import os
#assa
app = Flask(__name__)

@app.route("/")
def home():
    return jsonify(
        service="python-flask-app",
        status="running",
        message="Hello from Harness CI/CD pipeline 🚀"
    )

@app.route("/health")
def health():
    return jsonify(status="healthy"), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
