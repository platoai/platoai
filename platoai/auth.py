import os
import json


def credentials(url=None, token=None):
    """Get the credentials configuration from the
    `PLATOAI_APPLICATION_CREDENTIALS` environment variable.

    url can be overriden with the `PLATOAI_API_URL` environment variable.
    token can be overriden with the `PLATOAI_API_TOKEN` environment variable.

    Returns:
        dictionary: The contents of the :ref:`keyfile`.
    """
    if not url:
        url = os.getenv('PLATOAI_API_URL')

    if not token:
        token = os.getenv('PLATOAI_API_TOKEN')

    if not url or not token:
        with open(os.environ['PLATOAI_APPLICATION_CREDENTIALS'], 'r') as f:
            creds = json.loads(f.read())

        if not url:
            url = creds.get('url', 'https://api.platoai.com:9000')

        if not token:
            token = creds.get('token')

    assert token and url, 'Must provide token and url'

    return url, token
