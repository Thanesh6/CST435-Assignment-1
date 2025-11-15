import grpc
import pipeline_pb2
import pipeline_pb2_grpc
import time
import subprocess


def get_minikube_ip():
    try:
        result = subprocess.check_output(["minikube", "ip"]).decode().strip()
        return result
    except:
        return "127.0.0.1"  # fallback


def run_pipeline_client(data_size):
    print("=" * 60)
    print("🚀 STARTING Kubernetes gRPC CLIENT 🚀")
    print("=" * 60)

    # Get cluster IP
    minikube_ip = get_minikube_ip()
    master_port = 32354  # ← Your real NodePort
    master_address = f"{minikube_ip}:{master_port}"

    print(f"Connecting to MASTER service at: {master_address}")

    try:
        with grpc.insecure_channel(master_address) as channel:
            stub = pipeline_pb2_grpc.MasterServiceStub(channel)

            print(f"[{time.strftime('%H:%M:%S')}] CLIENT: Initiating pipeline with data_size = {data_size}...")
            request = pipeline_pb2.PipelineRequest(data_size=data_size)
            response = stub.RunPipeline(request)

            print(f"[{time.strftime('%H:%M:%S')}] CLIENT: Received final response from the master server.")
            print("-" * 25)
            print("✅ PIPELINE COMPLETE")
            print("-" * 25)

            # Parse response
            summary_parts = {}
            if response.summary:
                try:
                    parts = response.summary.split(', ')
                    for part in parts:
                        key, value = part.split('=')
                        summary_parts[key.strip()] = value.strip()
                except:
                    pass

            print("📊 Final Summary:")
            print(f"     - Cluster Result:   {summary_parts.get('Cluster', 'N/A')}")
            print(f"     - Correlation:      {float(summary_parts.get('Corr', 0.0)):.4f}")
            print(f"     - Average Distance: {float(summary_parts.get('Dist', 0.0)):.4f}")

            print(f"\n⏱️ Total Execution Time: {response.total_time:.4f} seconds")
            print("=" * 60)

    except grpc.RpcError as e:
        print("\n" + "="*60)
        print("❌ ERROR: Could not connect to the Kubernetes Master Service.")
        print(f"   Details: {e.code()} - {e.details()}")
        print("="*60)


if __name__ == '__main__':
    run_pipeline_client(300)
