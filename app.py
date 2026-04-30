from flask import Flask, request, jsonify, redirect
import random, string

app = Flask(__name__)
db = {}  # simple in-memory store

def generate_code():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))

@app.route('/shorten', methods=['POST'])
def shorten():
    data = request.get_json()
    url = data.get('url')
    if not url:
        return jsonify({'error': 'URL is required'}), 400
    code = generate_code()
    db[code] = url
    return jsonify({'short_url': f'http://localhost:5000/{code}'}), 201

@app.route('/<code>', methods=['GET'])
def redirect_url(code):
    url = db.get(code)
    if not url:
        return jsonify({'error': 'Not found'}), 404
    return redirect(url)

@app.route('/all', methods=['GET'])
def all_urls():
    return jsonify(db), 200

if __name__ == '__main__':
    app.run(debug=True)