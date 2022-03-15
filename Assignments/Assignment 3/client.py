import grpc

import payload_pb2
import payload_pb2_grpc
import pyspeedtest

PAYLOAD_SIZE = 1024 * 1024


def run(file_path: str):
    speed = pyspeedtest.SpeedTest("www.google.com")
    print(speed.download())
    input_file = open(file_path, 'rb')
    data = input_file.read(PAYLOAD_SIZE)
    while len(data) > 0:
        send_request(data, filename=file_path.split("/")[-1])
        data = input_file.read(PAYLOAD_SIZE)
    send_request(data, filename=file_path.split("/")[-1])
    input_file.close()


def send_request(data, filename):
    channel = grpc.insecure_channel('localhost:50051')
    # create a stub (client)
    stub = payload_pb2_grpc.SendAdaptivePayloadStub(channel)
    try:
        # create a valid request
        request = payload_pb2.Request(filename=filename, data=data)
        # make api call
        response = stub.data_transfer(request)
        print(response.status)
    except KeyboardInterrupt:
        channel.unsubscribe(close)
        exit()


def close(channel):
    channel.close()


if __name__ == "__main__":
    run("data/input/sample_data.csv")
