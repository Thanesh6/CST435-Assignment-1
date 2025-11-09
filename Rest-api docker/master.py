# --- START OF FILE master.py (Corrected) ---
from flask import Flask, request, jsonify
import requests
import time

app = Flask(__name__)

# Define the service URLs using the container names from docker-compose
WORKER1_URL = "http://worker1:5001/process"
WORKER2_URL = "http://worker2:5002/process"
WORKER3_URL = "http://worker3:5003/process"
WORKER4_URL = "http://worker4:5004/process"

@app.route("/run_pipeline", methods=["POST"])
def run_pipeline():
    start_time = time.time()
    data_size = request.json.get("data_size", 100)
    
    try:
        # Step 1: Call Worker 1 to generate data
        print(f"MASTER: Calling Worker 1 to generate data with size={data_size}")
        resp1 = requests.post(WORKER1_URL, json={"data_size": data_size})
        resp1.raise_for_status()  # Raise an exception for bad status codes
        data_from_w1 = resp1.json()
        
        # Step 2: Pass Worker 1's output to Worker 2 for normalization
        print("MASTER: Calling Worker 2 to normalize data")
        resp2 = requests.post(WORKER2_URL, json=data_from_w1)
        resp2.raise_for_status()
        data_from_w2 = resp2.json()
        
        # Step 3: Pass Worker 2's output to Worker 3 for feature extraction
        print("MASTER: Calling Worker 3 to extract features")
        resp3 = requests.post(WORKER3_URL, json=data_from_w2)
        resp3.raise_for_status()
        data_from_w3 = resp3.json()
        
        # Step 4: Pass Worker 3's output to Worker 4 for final analysis
        print("MASTER: Calling Worker 4 for final analysis")
        resp4 = requests.post(WORKER4_URL, json=data_from_w3)
        resp4.raise_for_status()
        final_result = resp4.json()

        total_time = time.time() - start_time
        
        # Return the final, meaningful summary from Worker 4
        return jsonify({
            "summary": final_result,
            "total_time": f"{total_time:.4f} seconds"
        })

    except requests.exceptions.RequestException as e:
        # Handle network or HTTP errors gracefully
        return jsonify({"error": "Failed to process pipeline", "details": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
# --- END OF FILE master.py (Corrected) ---