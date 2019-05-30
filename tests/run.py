from __future__ import print_function

import datetime
import os
import sys
from io import BytesIO
from pprint import pprint

import requests

import voxjar

if __name__ == "__main__":
    metadata = {
        "identifier": "test_call_identifier",
        "timestamp": datetime.datetime.now(),
        "type": {
            "identifier": "test_call_type_identifier",
            "name": "test_call_type_name",
        },
        "agents": [
            {
                "identifier": "test_agent_identifier",
                "name": "test_agent_name",
                "phoneNumber": 1234567890,
            }
        ],
        "customers": [
            {
                "identifier": "test_customer_identifier",
                "name": "test_customer_name",
                "phoneNumber": 9876543210,
            }
        ],
        "direction": "OUTGOING",
        "options": {"processAudio": True},
    }

    try:
        url = sys.argv[1]
    except IndexError:
        # yapf: disable
        url = "https://storage.googleapis.com/platoaiinc-audio-test/1-wav-gsm_ms-s16-8000"

    client = voxjar.Client(url=os.getenv("VOXJAR_API_URL", "https://api.voxjar.com:9001"))
    try:
        pprint(client.push(metadata, audio=BytesIO(requests.get(url).content)))
    except RuntimeError as e:
        print(e)
