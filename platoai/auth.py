import os
import json


def credentials():
    """Get the credentials configuration from the
    `PLATOAI_APPLICATION_CREDENTIALS` environment variable.

    Returns:
        dictionary: The contents of the :ref:`keyfile`.
    """
    with open(os.environ['PLATOAI_APPLICATION_CREDENTIALS'], 'r') as f:
        return json.loads(f.read())
