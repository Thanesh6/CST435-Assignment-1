from concurrent import futures
import grpc, pipeline_pb2, pipeline_pb2_grpc
import numpy as np
import time

class DataGenServicer(pipeline_pb2_grpc.DataGenServiceServicer):
    def GenerateData(self, request, context):
        start = time.time()
        size = request.size
        data = np.random.rand(size, size)
        flat_data = data.flatten().tolist()
        print(f"Generated matrix {size}x{size}")
        return pipeline_pb2.DataResponse(data=flat_data, rows=size, cols=size)

server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
pipeline_pb2_grpc.add_DataGenServiceServicer_to_server(DataGenServicer(), server)
server.add_insecure_port('[::]:50051')
server.start()
print("DataGenService running on port 50051")
server.wait_for_termination()
