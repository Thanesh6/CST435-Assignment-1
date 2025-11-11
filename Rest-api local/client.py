# --- START OF FILE client_heavy.py ---
import requests
import time

def run_pipeline_client(data_size):
    """
    Calls the local REST API master service (heavy compute) and prints a detailed summary.
    """
    master_url = "http://localhost:5000/run_pipeline"
    payload = {"data_size": data_size}

    print("=" * 60)
    print("🚀 STARTING LOCAL REST API CLIENT (HEAVY COMPUTE) 🚀")
    print("=" * 60)

    try:
        print(f"[{time.strftime('%H:%M:%S')}] CLIENT: Initiating pipeline with data_size = {data_size}...")
        
        # Make the HTTP POST request to the local master server
        response = requests.post(master_url, json=payload)
        response.raise_for_status()

        # Parse the JSON response from the server
        data = response.json()
        
        print(f"[{time.strftime('%H:%M:%S')}] CLIENT: Received final response from the master server.")
        print("-" * 25)
        print("✅ PIPELINE COMPLETE")
        print("-" * 25)

        # --- MODIFIED SECTION ---
        # Format the JSON data to match the gRPC/XML-RPC output style.
        summary = data.get("summary", {})
        
        print("📊 Final Summary:")
        print(f"     - Cluster Result:   {summary.get('cluster', 'N/A')}")
        print(f"     - Correlation:      {summary.get('correlation', 0.0):.4f}")
        print(f"     - Average Distance: {summary.get('avg_distance', 0.0):.4f}")
        
        print(f"\n⏱️ Total Execution Time: {data.get('total_time', '0.0')} seconds")
        print("=" * 60)

    except requests.exceptions.RequestException as e:
        print("\n" + "="*60)
        print("❌ ERROR: Could not connect to the local REST API Master Service.")
        print(f"   Please ensure the master.py script is running on port 5000.")
        print(f"   Details: {e}")
        print("="*60)

if __name__ == "__main__":
    # Define the size of the data for the pipeline.
    matrix_size = 300
    run_pipeline_client(matrix_size)
# --- END OF FILE client_heavy.py ---