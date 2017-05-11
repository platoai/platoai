import time
import grpc
from platoai_protos import api_pb2_grpc, api_pb2, phone_call_pb2


class PushRequestIter(object):
    """Wrapper that supports the iterator protocol to support streaming."""

    def __init__(self, audio, metadata, chunk_size=1024, callback=None):
        self.audio = audio
        self.metadata = metadata
        self.chunk_size = chunk_size
        self.callback = callback

    def __iter__(self):
        return self

    def next(self):
        chunk = self.audio.read(self.chunk_size)
        if chunk != '':
            phone_call = phone_call_pb2.PhoneCall(
                audio=chunk,
                metadata=phone_call_pb2.PhoneCallMetadata(**self.metadata))
            if self.callback:
                self.callback(self.chunk_size)
            return api_pb2.PushRequest(phoneCall=phone_call)
        else:
            raise StopIteration


def push(audio, metadata, host='api.platoai.com', port=9000, callback=None):
    t = metadata['timestamp']
    t = time.mktime(t.timetuple()) * 1e3 + t.microsecond / 1e3
    metadata['timestamp'] = long(t)

    channel = grpc.secure_channel('{}:{}'.format(host, port),
                                  grpc.ssl_channel_credentials())

    stub = api_pb2_grpc.ScoringStub(channel)
    stub.Push(PushRequestIter(audio, metadata, callback=callback))
