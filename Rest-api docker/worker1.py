# --- START OF FILE worker1.py (Corrected for Heavy Compute) ---
from flask import Flask, jsonify, request
import numpy as np

app = Flask(__name__)

@app.route('/process', methods=['POST'])
def process():
    data_size = request.json.get('data_size', 100)
    # Correctly generate a 2D matrix of floats
    matrix = np.random.rand(data_size, data_size)
    print(f"WORKER 1: Generated matrix {data_size}x{data_size}")
    return jsonify({
        "data": matrix.tolist(),
        "rows": data_size,
        "cols": data_size
    })

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001)
# --- END OF FILE worker1.py (Corrected for Heavy Compute) ---