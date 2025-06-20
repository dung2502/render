from flask import Flask, request, Response, render_template_string
import requests
import json
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Route mặc định để test GET trên trình duyệt
@app.route("/", methods=["GET"])
def home():
    return '✅ Flask app is running on Vercel! Use POST to fetch JSON from URL.'

# Route xử lý POST JSON
@app.route("/", methods=["POST"])
def process_json():
    data = request.get_json()
    url = data.get("url")

    if not url:
        return Response(
            json.dumps({"error": "Thiếu tham số 'url'"}, ensure_ascii=False),
            status=400,
            mimetype="application/json"
        )

    try:
        response = requests.get(url)
        response.raise_for_status()
        json_data = response.json()

        HTML_TEMPLATE = """
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Hiển thị dữ liệu</title>
        </head>
        <body>
            <h2>✅ Đã nhận được dữ liệu từ URL:</h2>
            <p><strong>URL:</strong> {{ url }}</p>
            <h3>Dữ liệu:</h3>
            <pre>{{ json_data | tojson(indent=2, ensure_ascii=False) }}</pre>
        </body>
        </html>
        """

        return render_template_string(HTML_TEMPLATE, url=url, json_data=json_data)

    except Exception as e:
        return Response(
            json.dumps({"error": str(e)}, ensure_ascii=False),
            status=500,
            mimetype="application/json"
        )

# ❌ Không dùng app.run() để Vercel có thể import
