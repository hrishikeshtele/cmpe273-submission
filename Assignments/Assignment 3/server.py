from concurrent import futures

import grpc

import payload_pb2
import payload_pb2_grpc


class Listener(payload_pb2_grpc.SendAdaptivePayloadServicer):
    MAXIMUM_SIZE_ALLOWED = 1024 * 1024 * 10
    data_dic = {}
    count = 0

    def data_transfer(self, request, context):
        file_name = request.filename
        input_bytes = request.data
        if len(input_bytes) == 0:
            self.count = 0
            self.write_file(file_name)
        else:
            if file_name not in self.data_dic:
                self.data_dic[file_name] = input_bytes
            else:
                self.data_dic[file_name] = self.data_dic[file_name] + input_bytes
            if len(self.data_dic[file_name]) > self.MAXIMUM_SIZE_ALLOWED:
                self.write_file(file_name)
                self.data_dic.pop(file_name)
        self.count += 1
        return payload_pb2.Response(status=True)

    def write_file(self, file_name):
        output_file = open("data/output/" + file_name, "ab+")
        output_file.write(self.data_dic[file_name])
        output_file.close()


def serve():
    # create a gRPC server
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
    payload_pb2_grpc.add_SendAdaptivePayloadServicer_to_server(Listener(), server)
    print('Starting server. Listening on port 50051.')
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
