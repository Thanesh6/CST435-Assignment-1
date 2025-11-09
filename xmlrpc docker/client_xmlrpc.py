import xmlrpc.client

master = xmlrpc.client.ServerProxy("http://localhost:8005")
resp = master.run_pipeline(300)
print("=== Final Response from XML-RPC Master ===")
print("Total Time:", resp["total_time"])
print("Summary:", resp["summary"])
