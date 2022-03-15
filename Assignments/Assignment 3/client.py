import grpc

import payload_pb2
import payload_pb2_grpc
import time


def run(file_path: str):
    payload_size = 1024 * 1024
    input_file = open(file_path, 'rb')
    data = input_file.read(payload_size)
    avg_response_time = 0
    chunk_no = 0
    initial_speed = 0
    while len(data) > 0:
        response_time = send_request(data, filename=file_path.split("/")[-1])
        avg_response_time = int((avg_response_time * chunk_no + response_time) / (chunk_no + 1))
        # print('avg_response_time', avg_response_time)
        if chunk_no == 0:
            initial_speed = (1024 * 1024) / avg_response_time
        else:
            payload_size = int(initial_speed * response_time)
        # upload_speed = int(speed.upload()/20.36)
        # print(upload_speed)
        chunk_no += 1
        print('payload_size', payload_size)
        data = input_file.read(payload_size)
    send_request(data, filename=file_path.split("/")[-1])
    input_file.close()


def send_request(data, filename):
    channel = grpc.insecure_channel('localhost:50051')
    # create a stub (client)
    stub = payload_pb2_grpc.SendAdaptivePayloadStub(channel)
    try:
        # create a valid request
        start = time.time()
        request = payload_pb2.Request(filename=filename, data=data)
        # make api call
        response = stub.data_transfer(request)
        return (time.time() - start) * 100
        # If avg response time is decreasing, decrease the payload, else increase the payload.
        # Maintain uniform speed, initial_speed = 1024*1024/time. Therefore, payload is initial_speed*time
    except KeyboardInterrupt:
        channel.unsubscribe(close)
        exit()


def close(channel):
    channel.close()


if __name__ == "__main__":
    run("data/input/sample_data.csv")
