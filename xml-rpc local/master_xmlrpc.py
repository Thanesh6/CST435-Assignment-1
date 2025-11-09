from xmlrpc.server import SimpleXMLRPCServer
import xmlrpc.client
import time

def run_pipeline(data_size):
    start = time.time()

    data_s = xmlrpc.client.ServerProxy("http://localhost:8001")
    pre_s = xmlrpc.client.ServerProxy("http://localhost:8002")
    feat_s = xmlrpc.client.ServerProxy("http://localhost:8003")
    ana_s = xmlrpc.client.ServerProxy("http://localhost:8004")

    data = data_s.generate_data(data_size)
    cleaned = pre_s.clean_data(data)
    features = feat_s.extract_features(cleaned)
    result = ana_s.analyze_data(features)

    total_time = time.time() - start
    summary = f"Cluster={result['cluster']}, Corr={result['correlation']:.3f}, Dist={result['avg_distance']:.3f}"
    print("Pipeline completed:", summary)
    return {"total_time": total_time, "summary": summary}

server = SimpleXMLRPCServer(("localhost", 8005))
server.register_function(run_pipeline, "run_pipeline")
print("MasterService (XML-RPC) running on port 8005")
server.serve_forever()
