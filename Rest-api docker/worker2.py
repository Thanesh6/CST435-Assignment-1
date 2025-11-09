from flask import Flask, jsonify, request
import numpy as np

app = Flask(__name__)

@app.route('/process', methods=['POST'])
def process():
    arr = np.array(request.json.get('data', []))
    norm = (arr - arr.min()) / (arr.max() - arr.min())
    return jsonify({"normalized": norm.tolist()})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002)
