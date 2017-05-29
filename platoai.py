import time
import io
from io import BytesIO
import grpc
from platoai_protos import api_pb2_grpc, api_pb2, phone_call_pb2


def _timestamp(dt):
    return time.mktime(dt.timetuple()) * 1e3 + dt.microsecond / 1e3


# TODO: ensure this supports streaming w/out reading entire file into RAM first
# TODO: why does inheriting from BytesIO not work?
class PushRequest(object):
    """Wrapper class for api_pb2.PushRequest that conforms to the iterator
    protocol to support streaming in the API.
    """

    def __init__(self,
                 metadata,
                 fileobj=None,
                 host='api.platoai.com',
                 port=9000,
                 channel=None,
                 chunk_size=1024,
                 callbacks=[]):
        self.metadata = metadata
        metadata['timestamp'] = long(_timestamp(metadata['timestamp']))

        if not fileobj:
            fileobj = BytesIO()
        self.buffer = fileobj

        if not channel:
            channel = grpc.secure_channel('{}:{}'.format(host, port),
                                          grpc.ssl_channel_credentials())
        self.stub = api_pb2_grpc.ScoringStub(channel)

        self.chunk_size = chunk_size
        self.callbacks = callbacks

    def __enter__(self):
        return self

    def __iter__(self):
        return iter(self)

    def write(self, chunk):
        return self.buffer.write(chunk)

    def next(self):
        chunk = self.buffer.read(self.chunk_size)

        if not chunk:
            raise StopIteration

        phone_call = phone_call_pb2.PhoneCall(
            audio=chunk,
            metadata=phone_call_pb2.PhoneCallMetadata(**self.metadata))

        for fn in self.callbacks:
            fn(self.chunk_size)

        return api_pb2.PushRequest(phoneCall=phone_call)

    def push(self):
        """Enqueue a call to be processed by Plato AI.

        Returns:
            metadata (:obj:`dictionary`): The metadata for the uploaded call or
                error details.
        """
        try:
            self.buffer.seek(0)
        except io.UnsupportedOperation:
            pass
        # TODO: handle errors?
        return self.stub.Push(self)

    def close(self):
        self.buffer.close()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


def push(audio,
         metadata,
         host='api.platoai.com',
         port=9000,
         channel=None,
         callbacks=[]):
    """Enqueue a call to be processed by Plato AI.

    Args:
        audio (:obj:`file-like object`): The raw audio bytes of the call.
        metadata (:obj:`dictionary`): The metadata for the call.
        channel (:obj:`grpc.channel`, optional): The gRPC channel.
        callbacks (list): A list of 1-arity functions, called with the chunk
            size after each chunk of audio is streamed to the API server.

    Returns:
        metadata (:obj:`dictionary`): The metadata for the uploaded call or
            error details.
    """
    with PushRequest(
            metadata,
            fileobj=audio,
            host=host,
            port=port,
            channel=channel,
            callbacks=callbacks) as push_request:
        return push_request.push()
