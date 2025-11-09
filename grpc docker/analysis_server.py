from concurrent import futures
import grpc, pipeline_pb2, pipeline_pb2_grpc
import numpy as np
import time

class AnalysisServicer(pipeline_pb2_grpc.AnalysisServiceServicer):
    def AnalyzeData(self, request, context):
        f = np.array(request.features)
        correlation = np.corrcoef(f) if len(f) > 1 else 1.0
        avg_distance = np.mean(np.abs(f - np.mean(f)))
        cluster = "Cluster A" if np.mean(f) > 0 else "Cluster B"
        print(f"Analysis done: {cluster}")
        return pipeline_pb2.AnalysisResponse(correlation=float(np.mean(correlation)),
                                             avg_distance=avg_distance,
                                             cluster_result=cluster)

server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
pipeline_pb2_grpc.add_AnalysisServiceServicer_to_server(AnalysisServicer(), server)
server.add_insecure_port('[::]:50054')
server.start()
print("AnalysisService running on port 50054")
server.wait_for_termination()
