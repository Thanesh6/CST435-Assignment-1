from concurrent import futures
import grpc, pipeline_pb2, pipeline_pb2_grpc
import time

class MasterServicer(pipeline_pb2_grpc.MasterServiceServicer):
    def RunPipeline(self, request, context):
        start = time.time()
        
        # Connect to each service
        data_stub = pipeline_pb2_grpc.DataGenServiceStub(grpc.insecure_channel('localhost:50051'))
        pre_stub = pipeline_pb2_grpc.PreprocessServiceStub(grpc.insecure_channel('localhost:50052'))
        feat_stub = pipeline_pb2_grpc.FeatureServiceStub(grpc.insecure_channel('localhost:50053'))
        ana_stub = pipeline_pb2_grpc.AnalysisServiceStub(grpc.insecure_channel('localhost:50054'))
        
        data = data_stub.GenerateData(pipeline_pb2.DataRequest(size=request.data_size))
        cleaned = pre_stub.CleanData(data)
        features = feat_stub.ExtractFeatures(cleaned)
        result = ana_stub.AnalyzeData(features)
        
        total_time = time.time() - start
        summary = f"Cluster={result.cluster_result}, Corr={result.correlation:.3f}, Dist={result.avg_distance:.3f}"
        print("Pipeline completed:", summary)
        return pipeline_pb2.PipelineResponse(total_time=total_time, summary=summary)

server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
pipeline_pb2_grpc.add_MasterServiceServicer_to_server(MasterServicer(), server)
server.add_insecure_port('[::]:50055')
server.start()
print("MasterService running on port 50055")
server.wait_for_termination()
