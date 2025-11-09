from xmlrpc.server import SimpleXMLRPCServer
import numpy as np

def generate_data(size):
    data = np.random.rand(size, size).tolist()
    print(f"Generated matrix {size}x{size}")
    return {"data": data, "rows": size, "cols": size}

server = SimpleXMLRPCServer(("0.0.0.0", 8001))
server.register_function(generate_data, "generate_data")
print("DataGenService (XML-RPC) running on port 8001")
server.serve_forever()