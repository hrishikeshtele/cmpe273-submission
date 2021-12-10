import json
from concurrent import futures

import grpc
import pymongo
import config

import replicator_pb2
import replicator_pb2_grpc


class Listener(replicator_pb2_grpc.DBReplicatorServicer):

    def execute_query(self, request, context):
        query = request.transaction

        mongo_client = pymongo.MongoClient(config.MONGO_DATABASE_CONFIG["host"], config.MONGO_DATABASE_CONFIG["port"])
        mongo_db = mongo_client["college"]

        dictionary = json.loads(query)

        for row in dictionary['change']:
            collection = mongo_db['students']
            if row['kind'] == 'insert' and row['table'] == 'students':
                col = {}
                for i in range(len(row['columnnames'])):
                    col[row['columnnames'][i]] = row['columnvalues'][i]
                collection.insert_one(col)
                print("Student collection inserted", col)

            elif row['kind'] == 'update' and row['table'] == 'students':
                student_id = row['oldkeys']['keyvalues'][0]
                doc = {}
                for i in range(len(row['columnnames'])):
                    doc[row['columnnames'][i]] = row['columnvalues'][i]
                collection.find_one_and_update({'id': student_id}, {'$set': doc})
                print("Student collection updated", doc)

            elif row['kind'] == 'delete' and row['table'] == 'students':
                doc = {}
                old_dict = row['oldkeys']
                for i in range(len(old_dict['keynames'])):
                    doc[old_dict['keynames'][i]] = old_dict['keyvalues'][i]
                collection.find_one_and_delete(doc)
                print("Student collection deleted", doc)

            else:
                print("Unknown operation")
                return replicator_pb2.Response(status=False)

        return replicator_pb2.Response(status=True)


def serve():
    # create a gRPC server
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))

    replicator_pb2_grpc.add_DBReplicatorServicer_to_server(Listener(), server)

    print('Starting server. Listening on port 50051.')
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
