# platoai

> Python implementation of the [Plato AI](https://platoai.com/) [API](http://api.platoai.com:3001/graphiql).

## installation

```
pip install platoai
```

## usage

```python
from __future__ import print_function
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

with open('test.wav', 'rb') as f:
    print(platoai.push(metadata, f))
```
