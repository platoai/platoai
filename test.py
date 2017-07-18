from __future__ import print_function
import os
import datetime
import time
import requests
import grpc
import platoai
from tqdm import tqdm

# TODO: improve testing...


def test_local(metadata, file_name='test.wav', channel=None):
    with open(file_name, 'rb') as f:
        with tqdm(total=os.path.getsize(file_name)) as pbar:
            try:
                pbar.write(
                    str(
                        platoai.push(
                            audio=f,
                            metadata=metadata,
                            callbacks=[pbar.update],
                            channel=channel)))
            except grpc.RpcError as e:
                pbar.write(e)


def test_remote_simple(metadata,
                       url='https://students.cs.byu.edu/~wmyers7/test.wav',
                       channel=None):
    download_request = requests.get(url, stream=True)
    r = requests.head(url)  # TODO: shouldnt need a separate head request
    with tqdm(total=int(r.headers['content-length'])) as pbar:
        try:
            pbar.write(
                str(
                    platoai.push(
                        audio=download_request.raw,
                        metadata=metadata,
                        callbacks=[pbar.update],
                        channel=channel)))
        except grpc.RpcError as e:
            pbar.write(e)


def test_remote_complex(metadata,
                        url='https://students.cs.byu.edu/~wmyers7/test.wav',
                        chunk_size=1024,
                        channel=None):
    download_request = requests.get(url, stream=True)
    r = requests.head(url)  # TODO: shouldnt need a separate head request
    with tqdm(total=int(r.headers['content-length'])) as pbar:
        with platoai.PushRequest(
                metadata,
                channel=channel,
                chunk_size=chunk_size,
                callbacks=[pbar.update]) as push_request:
            for chunk in download_request.iter_content(chunk_size=chunk_size):
                if chunk:
                    push_request.write(chunk)
            try:
                pbar.write(str(push_request.push()))
            except grpc.RpcError as e:
                pbar.write(e)


if __name__ == '__main__':
    now = datetime.datetime.now()

    metadata = {
        'id':
            'test_call_id_{}'.format(
                long(
                    time.mktime(now.timetuple()) * 1e3 + now.microsecond / 1e3)
            ),
        'timestamp':
            now,
        'callCenter': {
            'id': '-KjyJwwMAn32WSsaDgbF'
        },
        'agents': [{
            'id': 'test_agent_id',
            'name': 'test_agent_name',
            'phoneNumber': 1234567890
        }],
        'customers': [{
            'id': 'test_customer_id',
            'name': 'test_customer_name',
            'phoneNumber': 9876543210
        }],
        'direction':
            'OUTGOING'
    }

    test_local(metadata)
    # test_local(metadata, channel=grpc.insecure_channel('0.0.0.0:9001'))
    # test_remote_simple(metadata, channel=grpc.insecure_channel('0.0.0.0:9001'))
    # test_remote_complex(metadata, channel=grpc.insecure_channel('0.0.0.0:9001'))
