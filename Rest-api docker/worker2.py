# --- START OF FILE worker2.py (Corrected for Heavy Compute) ---
from flask import Flask, jsonify, request
import numpy as np

app = Flask(__name__)

@app.route('/process', methods=['POST'])
def process():
    # Reshape the incoming data back into a 2D matrix
    req_data = request.json
    matrix = np.array(req_data.get('data')).reshape(req_data.get('rows'), req_data.get('cols'))
    
    # Perform Z-Score Normalization
    mean = np.mean(matrix)
    std = np.std(matrix)
    normalized_matrix = (matrix - mean) / (std + 1e-8)
    
    print(f"WORKER 2: Normalized data (mean={mean:.3f}, std={std:.3f})")
    return jsonify({
        "data": normalized_matrix.flatten().tolist(), # Flatten for easy JSON transport
        "rows": req_data.get('rows'),
        "cols": req_data.get('cols')
    })

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002)
# --- END OF FILE worker2.py (Corrected for Heavy Compute) ---