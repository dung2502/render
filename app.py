from flask import Flask, request, Response
import requests
import json
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/", methods=["GET"])
def home():
    return '✅ Flask JSON Proxy is running. POST {"url": "<json file url>"} to get data.'

@app.route("/", methods=["POST"])
def process_json():
    try:
        data = request.get_json()
        url = data.get("url")

        if not url:
            return Response(
                json.dumps({"error": "Thiếu tham số 'url'"}, ensure_ascii=False),
                status=400,
                mimetype="application/json"
            )

        # Gửi GET request đến URL (thường là Google Drive export link)
        response = requests.get(url)
        response.raise_for_status()

        # Parse JSON từ nội dung tải về
        json_data = response.json()

        return Response(
            json.dumps(json_data, ensure_ascii=False),
            mimetype="application/json"
        )

    except Exception as e:
        print(f"[ERROR] {e}")
        return Response(
            json.dumps({"error": str(e)}, ensure_ascii=False),
            status=500,
            mimetype="application/json"
        )
