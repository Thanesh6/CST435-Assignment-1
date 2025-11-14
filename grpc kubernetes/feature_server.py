from concurrent import futures
import grpc, pipeline_pb2, pipeline_pb2_grpc
import numpy as np
import time

class FeatureServicer(pipeline_pb2_grpc.FeatureServiceServicer):
    def ExtractFeatures(self, request, context):
        data = np.array(request.data).reshape(request.rows, request.cols)
        eigvals = np.linalg.eigvals(data @ data.T)
        rank = np.linalg.matrix_rank(data)
        features = np.concatenate([eigvals.real[:10], [rank]])  # limit to 10 eigenvalues
        print(f"Extracted features (rank={rank})")
        return pipeline_pb2.FeatureResponse(features=features.tolist())

server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
pipeline_pb2_grpc.add_FeatureServiceServicer_to_server(FeatureServicer(), server)
server.add_insecure_port('[::]:50053')
server.start()
print("FeatureService running on port 50053")
server.wait_for_termination()
