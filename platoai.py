import time
import grpc
from platoai_protos import api_pb2_grpc, api_pb2, phone_call_pb2


class PushRequestIter(object):
    """Wrapper class for api_pb2.PushRequest that conforms to the iterator
    protocol to support streaming in the API.
    """

    def __init__(self, audio, metadata, chunk_size=1024, callbacks=[]):
        self.audio = audio

        self.metadata = metadata
        dt = metadata['timestamp']
        dt = time.mktime(dt.timetuple()) * 1e3 + dt.microsecond / 1e3
        metadata['timestamp'] = long(dt)

        self.chunk_size = chunk_size
        self.callbacks = callbacks

    def __iter__(self):
        return self

    def next(self):
        chunk = self.audio.read(self.chunk_size)
        if chunk:
            phone_call = phone_call_pb2.PhoneCall(
                audio=chunk,
                metadata=phone_call_pb2.PhoneCallMetadata(**self.metadata))

            for fn in self.callbacks:
                fn(self.chunk_size)

            return api_pb2.PushRequest(phoneCall=phone_call)
        else:
            raise StopIteration


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

    if not channel:
        channel = grpc.secure_channel('{}:{}'.format(host, port),
                                      grpc.ssl_channel_credentials())

    stub = api_pb2_grpc.ScoringStub(channel)
    return stub.Push(PushRequestIter(audio, metadata, callbacks=callbacks))
