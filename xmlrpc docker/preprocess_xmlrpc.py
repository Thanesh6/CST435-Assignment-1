from xmlrpc.server import SimpleXMLRPCServer
import numpy as np

def clean_data(data_dict):
    data = np.array(data_dict["data"])
    mean = float(np.mean(data))
    std = float(np.std(data))
    normalized = ((data - mean) / (std + 1e-8)).tolist()
    print(f"Data normalized (mean={mean:.3f}, std={std:.3f})")
    return {"data": normalized, "rows": data_dict["rows"], "cols": data_dict["cols"]}

# Listen on all available network interfaces
server = SimpleXMLRPCServer(("0.0.0.0", 8002))
server.register_function(clean_data, "clean_data")
print("PreprocessService (XML-RPC) running on port 8002")
server.serve_forever()
