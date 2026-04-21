from flask import Flask, jsonify,request
import os
from google.cloud import storage


app = Flask(__name__)

@app.get("/")
def health_check():
    return jsonify({"status": "ok", "service": "api-gcp"})

@app.get("/hello")
def hello():
    return jsonify({"message": "Hello from Flask on Cloud Run!"})

@app.get("/files")
def get_files():
    bucket_name = request.args.get("bucket") or os.environ.get("BUCKET_NAME")
    prefix = request.args.get("prefix", "")

    if not bucket_name:
        return jsonify({
            "error": "Bucket nao informado. Use ?bucket=nome ou defina BUCKET_NAME."
        }), 400

    try:
        client = storage.Client()
        blobs = client.list_blobs(bucket_name, prefix=prefix)
        items = [b.name for b in blobs]
        return jsonify({
            "bucket": bucket_name,
            "prefix": prefix,
            "count": len(items),
            "items": items
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)