from concurrent import futures

import grpc

import payload_pb2
import payload_pb2_grpc


class Listener(payload_pb2_grpc.SendAdaptivePayloadServicer):

    def data_transfer(self, request, context):

        return payload_pb2.Response(status=True)


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
