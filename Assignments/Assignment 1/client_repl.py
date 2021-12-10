import json

import grpc

import replicator_pb2
import replicator_pb2_grpc
import wal_reader


def run():
    # Read log file
    log_file = open("wal_log.txt", "r")
    log_lines = wal_reader.read_file(log_file)
    json_str = ''
    for line in log_lines:
        json_str += line
        try:
            log_data = json.loads(json_str)
            send_request(json.dumps(log_data))
            json_str = ''
        except ValueError:
            continue


def send_request(data):
    channel = grpc.insecure_channel('localhost:50051')
    # create a stub (client)
    stub = replicator_pb2_grpc.DBReplicatorStub(channel)
    try:
        # create a valid request
        request = replicator_pb2.Request(transaction=data)
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
