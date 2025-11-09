import grpc
import pipeline_pb2
import pipeline_pb2_grpc

def run_pipeline_client(data_size):
    """
    Connects to the MasterService and initiates the pipeline execution.
    """
    with grpc.insecure_channel('localhost:50055') as channel:
        stub = pipeline_pb2_grpc.MasterServiceStub(channel)
        print(f"Requesting pipeline run with data_size={data_size}...")
        
        request = pipeline_pb2.PipelineRequest(data_size=data_size)
        response = stub.RunPipeline(request)
        
        print("\n--- Pipeline Results ---")
        print(f"Total execution time: {response.total_time:.4f} seconds")
        print(f"Analysis Summary: {response.summary}")
        print("------------------------\n")

if __name__ == '__main__':
    matrix_size = 50 
    run_pipeline_client(matrix_size)
