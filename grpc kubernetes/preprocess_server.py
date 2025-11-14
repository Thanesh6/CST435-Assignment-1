from concurrent import futures
import grpc, pipeline_pb2, pipeline_pb2_grpc
import numpy as np
import time

class PreprocessServicer(pipeline_pb2_grpc.PreprocessServiceServicer):
    def CleanData(self, request, context):
        data = np.array(request.data).reshape(request.rows, request.cols)
        mean = np.mean(data)
        std = np.std(data)
        data = (data - mean) / (std + 1e-8)
        print(f"Data normalized (mean={mean:.3f}, std={std:.3f})")
        return pipeline_pb2.DataResponse(data=data.flatten().tolist(), rows=request.rows, cols=request.cols)

server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
pipeline_pb2_grpc.add_PreprocessServiceServicer_to_server(PreprocessServicer(), server)
server.add_insecure_port('[::]:50052')
server.start()
print("PreprocessService running on port 50052")
server.wait_for_termination()
