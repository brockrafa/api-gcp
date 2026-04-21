from flask import Flask, jsonify
import os

app = Flask(__name__)

@app.get("/")
def health_check():
    return jsonify({"status": "ok", "service": "api-gcp"})

@app.get("/hello")
def hello():
    return jsonify({"message": "Hello from Flask on Cloud Run!"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)