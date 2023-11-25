from flask import Flask, render_template, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask import make_response

"""The rate limit function is not working as intended currently. This is an experimental application. 
The current issue could be due to a specified memory route not being explicitly set."""

app = Flask(__name__)
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"],
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_numbers', methods=['POST'])
@limiter.limit("1/second", override_defaults=True)
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
