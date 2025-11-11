# --- START OF FILE worker4.py (Corrected for Heavy Compute) ---
from flask import Flask, jsonify, request
import numpy as np

app = Flask(__name__)

@app.route('/process', methods=['POST'])
def process():
    features = np.array(request.json.get('features', []))
    
    # Perform the same analysis as the other pipelines
    corr = np.mean(np.corrcoef(features)) if len(features) > 1 else 1.0
    avg_dist = np.mean(np.abs(features - np.mean(features)))
    cluster = "Cluster A" if np.mean(features) > 0 else "Cluster B"
    
    print(f"WORKER 4: Analysis done: {cluster}")
    return jsonify({
        "cluster": cluster,
        "correlation": float(corr),
        "avg_distance": float(avg_dist)
    })

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5004)
# --- END OF FILE worker4.py (Corrected for Heavy Compute) ---