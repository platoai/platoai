# platoai-python

Python implementation of the [Plato AI API](https://github.com/platoai/protos).

## requirements
[python](https://www.python.org/downloads/) v2.7+ (for the moment)

## installation

```
pip install git+git://github.com/platoai/platoai-python.git

```

## usage

```python
from __future__ import print_function
import datetime
import platoai

metadata = {
    'id': 'callId',
    'timestamp': datetime.datetime.now(),
    'callCenter': {
        'id': 'callCenterId'
    },
    'agents': [{
        'id': 'agentId',
        'name': 'Agent Name',
        'phoneNumber': 1234567890
    }],
    'customers': [{
        'id': 'customerId',
        'name': 'Customer Name',
        'phoneNumber': 9876543210
    }],
    'direction': 'OUTGOING'
}

with open('test.wav', 'rb') as f:
    print(platoai.push(f, metadata))
```

Add a progress bar (requires [`tqdm`](https://github.com/tqdm/tqdm)):
```python
from __future__ import print_function
import os
import platoai
from tqdm import tqdm

file_name = 'test.wav'
with open(file_name, 'rb') as f:
    with tqdm(total=os.path.getsize(file_name)) as pbar:
        print(platoai.push(f, metadata, callbacks=[pbar.update]))
```
