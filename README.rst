doitlater
=========

Schedule your HTTP-requests to run in the future.
::

    {
        'when': '2 hours from now',
        'request': {
            'url': 'https://example.com/post-new-message',
            'method': 'POST',
            'auth': 'hello:world',
            'headers': {
                'Accept': '*/*',
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3)'
            },
            'body': 'I can be a string or a dictionary(JSON Object)\
                     in the latter case I'll be converted to form-data.'
        },
        'hook': 'http://example2.com/post-results'

    }