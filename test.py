from __future__ import print_function
import os
import datetime
import grpc
import platoai
from tqdm import tqdm

# TODO: improve testing...

metadata = {
    'id': 'test',
    'timestamp': datetime.datetime.now(),
    'callCenter': {
        'id': 'test'
    },
    'agents': [{
        'id': 'test',
        'name': 'test',
        'phoneNumber': 1234567890
    }],
    'customers': [{
        'id': 'test',
        'name': 'test',
        'phoneNumber': 9876543210
    }],
    'direction': 'OUTGOING'
}

file_name = 'test.wav'
with open(file_name, 'rb') as f:
    with tqdm(total=os.path.getsize(file_name)) as pbar:
        print(platoai.push(
            f,
            metadata,
            channel=grpc.insecure_channel('0.0.0.0:9001'),
            callbacks=[pbar.update]))
