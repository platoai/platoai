from __future__ import print_function
import os
import datetime
import time
from pprint import pprint
# import json
import platoai

if __name__ == '__main__':
    now = datetime.datetime.now()

    metadata = {
        'identifier': 'test_call_identifier',
        'timestamp': now,
        'company': {
            'id': 'b87cc8ea-6820-11e7-891e-4f389aefc782'
        },
        'type': {
            'identifier': 'test_call_type_identifier',
            'name': 'test_call_type_name'
        },
        'agents': [{
            'identifier': 'test_agent_identifier',
            'name': 'test_agent_name',
            'phoneNumber': 1234567890
        }],
        'customers': [{
            'identifier': 'test_customer_identifier',
            'name': 'test_customer_name',
            'phoneNumber': 9876543210
        }],
        'direction': 'OUTGOING'
    }

    url = os.getenv('PLATOAI_API_URL', 'http://localhost:9001')
    with open('./test.wav', 'rb') as f:
        client = platoai.Client(url=url, token='faketoken')
        try:
            pprint(client.push(metadata, audio=f))
        except RuntimeError as e:
            print(e)
