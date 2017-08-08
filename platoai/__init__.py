import os
import json
from platoai.push_request import PushRequest
import gql
from platoai.transport import HttpTransport
import platoai.auth


class Client(object):
    """Plato AI API client.

    Args:
        url (str, optional): The URL for the API.
        token (str, optional): The JWT authenticating this Client to the API.
        timeout (int, optional): The timeout for API calls.
    """

    def __init__(self, url=None, token=None, timeout=None):
        if not url or not token:
            creds = platoai.auth.credentials()

            if not url:
                url = creds.get('url', 'https://api.platoai.com:9000')

            if not token:
                token = creds['token']

        self.url = url
        self.token = token

        self._client = gql.Client(
            transport=HttpTransport('{}/graphql'.format(url), token, timeout),
            fetch_schema_from_transport=True)

    def push_request(self, metadata, audio=None):
        """A file-like object used to enqueue a call audio file to be processed
        by Plato AI.

        Args:
            metadata (dict): The metadata for the call.
            audio (file): The raw audio bytes of the call.
        Returns:
            metadata (dict): The metadata for the uploaded call.
        Example:
            .. code:: python

                import datetime
                import requests
                import platoai

                metadata = {
                    'identifier': 'callId',
                    'type': {
                        'identifier': 'typeIdentifier',
                        'name': 'typeName',
                    },
                    'timestamp': datetime.datetime.now(),
                    'company': {
                        'id': 'companyId'
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
        return PushRequest(self.token, metadata, audio=audio, url=self.url)

    def push(self, metadata, audio):
        """Enqueue a call to be processed by Plato AI.

        Args:
            metadata (dict): The metadata for the call.
            audio (file): The raw audio bytes of the call.
        Returns:
            metadata (dict): The metadata for the uploaded call.
        Example:
            .. code:: python

                import datetime
                import platoai

                metadata = {
                    'identifier': 'callId',
                    'type': {
                        'identifier': 'typeIdentifier',
                        'name': 'typeName',
                    },
                    'timestamp': datetime.datetime.now(),
                    'company': {
                        'id': 'companyId'
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
        with PushRequest(self.token, metadata, audio, self.url) as push_request:
            return push_request.push()

    def execute(self, document, *args, **kwargs):
        return self._client.execute(document, *args, **kwargs)
