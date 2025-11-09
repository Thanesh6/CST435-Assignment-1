from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/process', methods=['POST'])
def process():
    features = request.json.get('features', {})
    result = "High variance" if features["std"] > 0.25 else "Stable"
    return jsonify({"analysis": result})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5004)
