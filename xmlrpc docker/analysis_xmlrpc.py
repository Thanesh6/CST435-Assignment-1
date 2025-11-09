from xmlrpc.server import SimpleXMLRPCServer
import numpy as np

def analyze_data(feature_dict):
    f = np.array(feature_dict["features"])
    corr = float(np.mean(np.corrcoef(f))) if len(f) > 1 else 1.0
    avg_dist = float(np.mean(np.abs(f - np.mean(f))))
    cluster = "Cluster A" if np.mean(f) > 0 else "Cluster B"
    print(f"Analysis done: {cluster}")
    return {"correlation": corr, "avg_distance": avg_dist, "cluster": cluster}

# Listen on all available network interfaces
server = SimpleXMLRPCServer(("0.0.0.0", 8004))
server.register_function(analyze_data, "analyze_data")
print("AnalysisService (XML-RPC) running on port 8004")
server.serve_forever()
