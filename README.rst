platoai
=======

.. image:: https://readthedocs.org/projects/platoai/badge/?version=latest
   :target: http://platoai.readthedocs.io/en/latest/?badge=latest
|

    Python implementation of the `Plato AI`_ `API`_.

installation
------------

::

    pip install platoai


usage
-----

.. code:: python

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


.. _Plato AI: https://platoai.com/
.. _API: https://api.platoai.com:9000/graphiql
