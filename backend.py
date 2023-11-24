from flask import Flask, render_template, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask import make_response

app = Flask(__name__)
limiter = Limiter(app, key_func=get_remote_address)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_numbers', methods=['POST'])
@limiter.limit("2 per second")
def generate_numbers():
    # Process the request and send random numbers back
    import random
    numbers = [random.randint(1, 100) for _ in range(5)]
    return jsonify(numbers)

@limiter.request_filter
def exempt_users():
    # You can customize this function to exempt certain users from rate limiting
    return False

@limiter.request_filter
def custom_response():
    # Customize the response when rate limit is exceeded
    response = make_response(jsonify({"error": "Rate limit exceeded"}), 429)
    response.headers['Content-Type'] = 'application/json'
    return response

app.run(host='0.0.0.0', port=5000, debug=True)
