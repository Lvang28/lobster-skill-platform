"""
最小化测试应用 - 用于诊断问题
"""
from flask import Flask, jsonify

app = Flask(__name__)
app.secret_key = 'test_secret_key'

@app.route('/')
def index():
    return jsonify({
        'status': 'ok',
        'message': 'Flask is working!'
    })

@app.route('/health')
def health():
    return jsonify({
        'status': 'healthy',
        'database': 'not_connected',
        'message': 'Minimal test endpoint'
    })

if __name__ == '__main__':
    print("🧪 Starting minimal Flask app...")
    app.run(host='0.0.0.0', port=10000, debug=False)
