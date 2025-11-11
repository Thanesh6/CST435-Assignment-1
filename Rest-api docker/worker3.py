# --- START OF FILE worker3.py (Corrected for Heavy Compute) ---
from flask import Flask, jsonify, request
import numpy as np

app = Flask(__name__)

@app.route('/process', methods=['POST'])
def process():
    # Reshape the incoming data back into a 2D matrix
    req_data = request.json
    matrix = np.array(req_data.get('data')).reshape(req_data.get('rows'), req_data.get('cols'))

    # --- PERFORM THE HEAVY COMPUTATION ---
    mat_mul = matrix @ matrix.T
    eigvals = np.linalg.eigvals(mat_mul)
    rank = np.linalg.matrix_rank(matrix)
    
    # Extract the features, same as the other pipelines
    features = eigvals.real[:10].tolist() + [int(rank)]
    
    print(f"WORKER 3: Extracted features (rank={rank})")
    return jsonify({"features": features})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5003)
# --- END OF FILE worker3.py (Corrected for Heavy Compute) ---