import os
import json
from platoai.push_request import PushRequest


class Client(object):
    """Plato AI API client.
    Args:
        url (str, optional): The URL for the API.
    """

    def __init__(self, url=None, token=None):
        if not url or not token:
            with open(os.environ['PLATOAI_APPLICATION_CREDENTIALS'], 'r') as f:
                config = json.loads(f.read())

                if not url:
                    url = config.get('url', 'https://api.platoai.com:9000')

                if not token:
                    token = config['token']

        self.url = url
        self.token = token

    def push_request(self, metadata, audio=None):
        """A file-like object used to enqueue a call audio file to be processed
        by Plato AI.

        Args:
            metadata (:obj:`dictionary`): The metadata for the call.
            audio (:obj:`file-like object`): The raw audio bytes of the call.
        Returns:
            metadata (:obj:`dictionary`): The metadata for the uploaded call.
        Example:
            .. code:: python

                import datetime
                import requests
                import platoai

                metadata = {
                    'identifier': 'callId',
                    'timestamp': datetime.datetime.now(),
                    'company': {
                        'identifier': 'companyId'
                    },
                    'agents': [{
                        'identifier': 'agentId',
                        'name': 'Agent Name',
                        'phoneNumber': 1234567890
                    }],
                    'customers': [{
                        'identifier': 'customerId',
                        'name': 'Customer Name',
                        'phoneNumber': 9876543210
                    }],
                    'direction': 'OUTGOING'
                }

                client = platoai.Client()

                r = requests.get('https://somesource.com', stream=True)
                with client.push_request(metadata) as push_request:
                    for chunk in r.iter_content(chunk_size=1024):
                        push_request.write(chunk)
                    push_request.push()

        """
        return PushRequest(metadata, audio=audio, url=self.url)

    def push(self, metadata, audio):
        """Enqueue a call to be processed by Plato AI.

        Args:
            metadata (:obj:`dictionary`): The metadata for the call.
            audio (:obj:`file-like object`): The raw audio bytes of the call.
        Returns:
            metadata (:obj:`dictionary`): The metadata for the uploaded call.
        Example:
            .. code:: python

                import datetime
                import platoai

                metadata = {
                    'identifier': 'callId',
                    'timestamp': datetime.datetime.now(),
                    'company': {
                        'identifier': 'companyId'
                    },
                    'agents': [{
                        'identifier': 'agentId',
                        'name': 'Agent Name',
                        'phoneNumber': 1234567890
                    }],
                    'customers': [{
                        'identifier': 'customerId',
                        'name': 'Customer Name',
                        'phoneNumber': 9876543210
                    }],
                    'direction': 'OUTGOING'
                }

                client = platoai.Client()

                with open('test.wav', 'rb') as f:
                    client.push(metadata, f)
        """
        with PushRequest(metadata, audio=audio, url=self.url) as push_request:
            return push_request.push()
