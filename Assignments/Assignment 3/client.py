import csv
import time

import grpc
import speedtest

import payload_pb2
import payload_pb2_grpc


def run(file_path: str):
    payload_size = 1024 * 512
    input_file = open(file_path, 'rb')
    data = input_file.read(payload_size)
    chunk_no = 0
    initial_speed = 0
    header = ['Response_Time', 'Payload_Size']  # Making header for csv file
    li = []
    sum_response_time = 0
    while len(data) > 0:
        sum_response_time += send_request(data, filename=file_path.split("/")[-1])
        avg_response_time = sum_response_time / (chunk_no + 1)
        if chunk_no == 0:
            initial_speed = payload_size * avg_response_time
        else:
            payload_size = (initial_speed / avg_response_time)
        # Writing into sources.csv file
        li.append([avg_response_time, payload_size])
        chunk_no += 1
        print('payload_size', payload_size)
        data = input_file.read(int(payload_size))
    send_request(data, filename=file_path.split("/")[-1])
    # Opening the file with specific path. Please include your path inside open & before sources.csv file
    with open('sources.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        # Writing header to the CSV file
        writer.writerow(header)
        writer.writerows(li)
    input_file.close()


async def find_upload_speed():
    speed = speedtest.Speedtest()
    upload_speed = await int(speed.upload() / 20.36)
    return upload_speed


def send_request(data, filename):
    options = [('grpc.max_message_length', 100 * 1024 * 1024)]
    channel = grpc.insecure_channel('localhost:50051', options=options)
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
    start_time = time.time()
    run("data/input/sample_data.csv")
    print((time.time() - start_time))
