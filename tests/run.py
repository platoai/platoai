from __future__ import print_function
import os
import datetime
import time
from pprint import pprint
import json
import platoai

if __name__ == '__main__':
    now = datetime.datetime.now()

    metadata = {
        'identifier':
            'test_call_identifier_{}'
            .format(time.mktime(now.timetuple()) * 1e3 + now.microsecond / 1e3),
        'timestamp':
            now,
        'company': {
            'id': 'b87cf3e2-6820-11e7-8a5d-e7c85d5a5479'
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
        'direction':
            'OUTGOING'
    }

    url = os.getenv('PLATOAI_API_URL', 'http://localhost:3001/enqueue')
    with open('test.wav', 'rb') as f:
        r = platoai.push(metadata, fileobj=f, url=url)
        if not r:
            print('No response.')
        pprint(json.loads(r))
