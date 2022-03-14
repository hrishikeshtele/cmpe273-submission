import grpc

import payload_pb2
import payload_pb2_grpc
import pyspeedtest


def run():
    speed = pyspeedtest.SpeedTest("www.google.com")
    print(speed.download())


def send_request(data):
    channel = grpc.insecure_channel('localhost:50051')
    # create a stub (client)
    stub = payload_pb2_grpc.SendAdaptivePayloadStub(channel)
    try:
        # create a valid request
        request = payload_pb2.Request(data=data, filename="test.csv")
        # make api call
        response = stub.execute_query(request)
        print(response.status)
    except KeyboardInterrupt:
        channel.unsubscribe(close)
        exit()


def close(channel):
    channel.close()


if __name__ == "__main__":
    run()
