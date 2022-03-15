# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import payload_pb2 as payload__pb2


class SendAdaptivePayloadStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.data_transfer = channel.unary_unary(
                '/SendAdaptivePayload/data_transfer',
                request_serializer=payload__pb2.Request.SerializeToString,
                response_deserializer=payload__pb2.Response.FromString,
                )


class SendAdaptivePayloadServicer(object):
    """Missing associated documentation comment in .proto file."""

    def data_transfer(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_SendAdaptivePayloadServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'data_transfer': grpc.unary_unary_rpc_method_handler(
                    servicer.data_transfer,
                    request_deserializer=payload__pb2.Request.FromString,
                    response_serializer=payload__pb2.Response.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'SendAdaptivePayload', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class SendAdaptivePayload(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def data_transfer(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/SendAdaptivePayload/data_transfer',
            payload__pb2.Request.SerializeToString,
            payload__pb2.Response.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)