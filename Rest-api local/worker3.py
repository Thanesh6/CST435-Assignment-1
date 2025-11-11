# --- START OF FILE worker3_heavy.py ---
from flask import Flask, jsonify, request
import numpy as np

app = Flask(__name__)

@app.route('/process', methods=['POST'])
def process():
    # Reshape the incoming data back into a 2D matrix
    req_data = request.json
    matrix = np.array(req_data.get('data')).reshape(req_data.get('rows'), req_data.get('cols'))

    # --- PERFORM THE HEAVY COMPUTATION ---
    # 1. Matrix Multiplication (O(n^3))
    mat_mul = matrix @ matrix.T
    # 2. Eigenvalue Decomposition (O(n^3))
    eigvals = np.linalg.eigvals(mat_mul)
    # 3. Matrix Rank Calculation (O(n^3))
    rank = np.linalg.matrix_rank(matrix)
    
    # Extract the features, same as the other pipelines
    features = eigvals.real[:10].tolist() + [int(rank)]
    
    print(f"WORKER 3: Extracted features (rank={rank})")
    return jsonify({"features": features})

if __name__ == '__main__':
    app.run(port=5003)
# --- END OF FILE worker3_heavy.py ---