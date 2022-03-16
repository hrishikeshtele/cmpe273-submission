import grpc

import payload_pb2
import payload_pb2_grpc
import time
import threading
import speedtest
import asyncio
import csv

def run(file_path: str):
    payload_size = 1024 * 1024
    input_file = open(file_path, 'rb')
    data = input_file.read(payload_size)
    avg_response_time = 0
    chunk_no = 0
    initial_speed = 0
#     thr = threading.Thread(target=get_or_create_eventloop, args=(), kwargs={})
    header = ['Response_Time', 'Payload_Size'] #Making header for csv file
    li = []
    while len(data) > 0:
        response_time = send_request(data, filename=file_path.split("/")[-1])
        avg_response_time = ((avg_response_time * chunk_no + response_time) / (chunk_no + 1))
        print('avg_response_time', avg_response_time)
        if chunk_no == 0:
            initial_speed = (1024 * 1024) * avg_response_time
        else:
            payload_size = (initial_speed / avg_response_time)

        li.append([avg_response_time, payload_size ]) #Writing into sources.csv file
#         loop = get_or_create_eventloop()
#         upload_speed = asyncio.ensure_future(find_upload_speed())
# #         loop.run_forever()
#         print(upload_speed)

        # upload_speed = int(speed.upload()/20.36)
#         print(thr.start())
        chunk_no += 1
        print('payload_size', payload_size)
        data = input_file.read(int(payload_size))
    send_request(data, filename=file_path.split("/")[-1])
#     print(li)
    with open('sources.csv', 'w',  newline='', encoding='utf-8') as f: #Opening the file with specific path. Please include your path inside open & before sources.csv file
                writer = csv.writer(f)
                writer.writerow(header)       #Writing header to the CSV file
                writer.writerows(li)
    input_file.close()

def get_or_create_eventloop():
    try:
        return asyncio.get_event_loop()
    except RuntimeError as ex:
        if "There is no current event loop in thread" in str(ex):
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            return asyncio.get_event_loop()
async def find_upload_speed():
    speed  = speedtest.Speedtest()
    upload_speed = await int(speed.upload()/20.36)
    return upload_speed

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
    run("data/input/SherlockHolmes.docx")
