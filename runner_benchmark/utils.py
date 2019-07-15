import re


class QuestionnaireMixins:
    client = None
    csrf_token = None
    previous_url = None

    def get(self, *args, **kwargs):
        allow_redirects = kwargs.pop('allow_redirects', False)
        kwargs.pop('method', None)

        print('\nGET', kwargs['url'])

        response = self.client.get(allow_redirects=allow_redirects, *args, **kwargs)

        if not response.content:
            raise Exception(f"No content in GET response for url: {kwargs['url']}")

        self.csrf_token = _extract_csrf_token(response.content.decode('utf8'))
        self.previous_url = kwargs['url']

        print('csrf_token', self.csrf_token)

        return response

    def post(self, *args, **kwargs):
        data = kwargs.pop('data', {}) or {}
        kwargs.pop('method', None)
        allow_redirects = kwargs.pop('allow_redirects', False)

        data['csrf_token'] = self.csrf_token

        headers = {
            'Referer': self.previous_url
        }

        print('POST Headers', headers)

        response = self.client.post(allow_redirects=allow_redirects, headers=headers, data=data, *args, **kwargs)
        return response


CSRF_REGEX = re.compile(r'<input id=csrf_token name=csrf_token type=hidden value=(.+?)>')


def _extract_csrf_token(html):
    match = CSRF_REGEX.search(html)
    if match:
        return match.group(1)
