import requests
from graphql.execution import ExecutionResult
from graphql.language.printer import print_ast


class PlatoaiHTTPTransport(object):

    def __init__(self, url, token, timeout=None):
        """
        Args:
            url (str): The GraphQL URL
            timeout (int, optional): Specifies a default timeout for requests
                                     (Default: None)
        """
        self.url = url
        self.default_timeout = timeout
        self.token = token

    def execute(self, document, variable_values=None, timeout=None):
        payload = {
            'query': print_ast(document),
            'variables': variable_values or {}
        }

        # TODO: check for file objects: hasattr(fp, 'read')

        post_args = {
            'headers': {
                'Authorization': 'Bearer {}'.format(self.token)
            },
            'timeout': timeout or self.default_timeout,
            'json': payload
        }
        request = requests.post(self.url, **post_args)
        request.raise_for_status()

        result = request.json()
        assert 'errors' in result or 'data' in result,\
               'Received non-compatible response "{}"'.format(result)
        return ExecutionResult(
            errors=result.get('errors'), data=result.get('data'))
