Authentication
**************

.. _Overview:

Overview
========

Download a JSON `keyfile`_ and point to it using an environment variable:

.. code-block:: bash

    $ export VOXJAR_APPLICATION_CREDENTIALS="/path/to/keyfile.json"


.. _keyfile:

JSON Keyfile
============

Example:

.. code-block:: json

		{
			"url": "https://api.voxjar.com:9000/",
			"token": "token"
		}
