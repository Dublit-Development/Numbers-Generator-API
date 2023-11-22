from flask import Flask, render_template, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_numbers', methods=['POST'])
def generate_numbers():
    # Process the request and send random numbers back
    import random
    numbers = [random.randint(1, 100) for _ in range(5)]
    return jsonify(numbers)

if __name__ == '__main__':
    app.run(debug=True)
