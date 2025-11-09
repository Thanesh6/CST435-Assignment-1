from xmlrpc.server import SimpleXMLRPCServer
import numpy as np

def extract_features(data_dict):
    data = np.array(data_dict["data"])
    eigvals = np.linalg.eigvals(data @ data.T)
    rank = int(np.linalg.matrix_rank(data))
    features = eigvals.real[:10].tolist() + [rank]
    print(f"Extracted features (rank={rank})")
    return {"features": features}

# Listen on all available network interfaces
server = SimpleXMLRPCServer(("0.0.0.0", 8003))
server.register_function(extract_features, "extract_features")
print("FeatureService (XML-RPC) running on port 8003")
server.serve_forever()
