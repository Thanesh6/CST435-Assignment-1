from flask import Flask, jsonify, request
import numpy as np

app = Flask(__name__)

@app.route('/process', methods=['POST'])
def process():
    data = request.json.get('data_size', 100)
    arr = np.random.randint(0, 100, data)
    return jsonify({"data": arr.tolist()})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001)
