import time
from io import BytesIO
import datetime
import json
import requests

DEFAULT_URL = 'https://api.platoai.com:3000/enqueue'


def _serialize(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime.datetime, datetime.date)):
        serial = obj.isoformat()
        return serial
    raise TypeError("Type {} not serializable".format(type(obj)))


def _timestamp(dt):
    return time.mktime(dt.timetuple()) * 1e3 + dt.microsecond / 1e3


# TODO: ensure this supports streaming w/out reading entire file into RAM first
# TODO: use https://github.com/Julian/jsonschema to validate JSON schema
class PushRequest(object):
    """Wrapper class for api_pb2.PushRequest that conforms to the iterator
    protocol to support streaming in the API.
    """

    def __init__(self, metadata, fileobj=None, url=DEFAULT_URL):
        self.metadata = metadata
        metadata['timestamp'] = _timestamp(metadata['timestamp'])

        self.url = url

        if not fileobj:
            fileobj = BytesIO()
        self.buffer = fileobj

    def __enter__(self):
        return self

    def write(self, chunk):
        return self.buffer.write(chunk)

    def push(self):
        """Enqueue a call to be processed by Plato AI.

        Returns:
            metadata (:obj:`dictionary`): The metadata for the uploaded call or
                error details.
        """
        payload = json.dumps(self.metadata, default=_serialize)
        files = {
            'metadata': (None, payload, 'application/json'),
            'file': (self.metadata.get('identifier'), self.buffer,
                     'application/octet-stream')
        }
        return requests.post(self.url, files=files).content

    def close(self):
        self.buffer.close()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


def push(metadata, fileobj, url=DEFAULT_URL):
    """Enqueue a call to be processed by Plato AI.

    Args:
        audio (:obj:`file-like object`): The raw audio bytes of the call.
        metadata (:obj:`dictionary`): The metadata for the call.

    Returns:
        metadata (:obj:`dictionary`): The metadata for the uploaded call or
            error details.
    """
    with PushRequest(metadata, fileobj, url) as push_request:
        return push_request.push()
