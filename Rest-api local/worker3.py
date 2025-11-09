from flask import Flask, jsonify, request
import numpy as np

app = Flask(__name__)

@app.route('/process', methods=['POST'])
def process():
    arr = np.array(request.json.get('normalized', []))
    mean = float(np.mean(arr))
    std = float(np.std(arr))
    return jsonify({"features": {"mean": mean, "std": std}})

if __name__ == '__main__':
    app.run(port=5003)
