# --- START OF FILE client.py (for Heavy Compute REST API) ---
import requests
import time

def run_pipeline_client(data_size):
    """
    Calls the REST API master service and prints a detailed, formatted summary
    that is consistent with the gRPC and XML-RPC clients.
    """
    # This URL works for both local runs and Docker runs (via port mapping)
    master_url = "http://localhost:5000/run_pipeline"
    payload = {"data_size": data_size}

    print("=" * 60)
    print("🚀 STARTING REST API PIPELINE CLIENT (HEAVY COMPUTE) 🚀")
    print("=" * 60)

    try:
        print(f"[{time.strftime('%H:%M:%S')}] CLIENT: Initiating pipeline with data_size = {data_size}...")
        
        # Make the HTTP POST request to the master server
        response = requests.post(master_url, json=payload)
        response.raise_for_status()  # Raise an exception for bad status codes (like 404 or 500)

        # Parse the JSON response from the server
        data = response.json()
        
        print(f"[{time.strftime('%H:%M:%S')}] CLIENT: Received final response from the master server.")
        print("-" * 25)
        print("✅ PIPELINE COMPLETE")
        print("-" * 25)

        # --- Format the JSON data to match the gRPC/XML-RPC output style ---
        summary = data.get("summary", {})
        
        print("📊 Final Summary:")
        print(f"     - Cluster Result:   {summary.get('cluster', 'N/A')}")
        print(f"     - Correlation:      {summary.get('correlation', 0.0):.4f}")
        print(f"     - Average Distance: {summary.get('avg_distance', 0.0):.4f}")
        
        print(f"\n⏱️ Total Execution Time: {data.get('total_time', '0.0')} seconds")
        print("=" * 60)

    except requests.exceptions.RequestException as e:
        print("\n" + "="*60)
        print("❌ ERROR: Could not connect to the REST API Master Service.")
        print(f"   Please ensure the master server is running on localhost:5000.")
        print(f"   (For Docker, ensure the containers are running and port 5000 is exposed).")
        print(f"   Details: {e}")
        print("="*60)

if __name__ == "__main__":
    # Define the size of the data for the pipeline.
    matrix_size = 300
    run_pipeline_client(matrix_size)
# --- END OF FILE client.py (for Heavy Compute REST API) ---