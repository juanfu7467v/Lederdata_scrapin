from flask import Flask, jsonify
from flask_cors import CORS
from routes.telegram_api import telegram_bp

app = Flask(__name__, static_folder='static', static_url_path='/static')
CORS(app)

app.register_blueprint(telegram_bp, url_prefix='/api/telegram')

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/health')
def health():
    return jsonify({"ok": True, "service": "telegram_api_wrapper"})

if __name__ == "__main__":
    # For local dev only. In production use gunicorn.
    app.run(host="0.0.0.0", port=int(__import__('os').environ.get("PORT", 5000)))
