from flask import Flask, jsonify, request
import requests, time

app = Flask(__name__)

WORKERS = {
    "gen": "http://127.0.0.1:5001/process",
    "norm": "http://127.0.0.1:5002/process",
    "feat": "http://127.0.0.1:5003/process",
    "anal": "http://127.0.0.1:5004/process"
}

@app.route('/run_pipeline', methods=['POST'])
def run_pipeline():
    t0 = time.time()
    payload = request.json or {}

    # Step 1: Generate data
    step1 = requests.post(WORKERS["gen"], json=payload).json()

    # Step 2: Normalize
    step2 = requests.post(WORKERS["norm"], json=step1).json()

    # Step 3: Extract features
    step3 = requests.post(WORKERS["feat"], json=step2).json()

    # Step 4: Analyze
    step4 = requests.post(WORKERS["anal"], json=step3).json()

    t1 = time.time()
    return jsonify({
        "summary": step4,
        "total_time": round(t1 - t0, 3)
    })

if __name__ == '__main__':
    app.run(port=5000)
