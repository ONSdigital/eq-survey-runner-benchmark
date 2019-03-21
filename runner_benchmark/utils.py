import re


class QuestionnaireMixins:
    client = None
    csrftoken = None
    prevurl = None

    def get(self, *args, **kwargs):
        allow_redirects = kwargs.pop('allow_redirects', False)
        kwargs.pop('method', None)

        print('GET', kwargs['url'])

        response = self.client.get(allow_redirects=allow_redirects, *args, **kwargs)

        if not response.content:
            raise Exception(f"No content in GET response for url: {kwargs['url']}")

        self.csrftoken = _extract_csrf_token(response.content.decode('utf8'))
        self.prevurl = kwargs['url']

        print('csrftoken', self.csrftoken)

        return response

    def post(self, *args, **kwargs):
        data = kwargs.pop('data', {}) or {}
        kwargs.pop('method', None)
        allow_redirects = kwargs.pop('allow_redirects', False)

        data['csrf_token'] = self.csrftoken

        headers = {
            'Referer': self.prevurl
        }

        print('POST Headers', headers)

        response = self.client.post(allow_redirects=allow_redirects, headers=headers, data=data, *args, **kwargs)
        return response


CSRF_REGEX = re.compile(r'<input id="csrf_token" name="csrf_token" type="hidden" value="(.+?)"/>')


def _extract_csrf_token(html):
    match = CSRF_REGEX.search(html)
    if match:
        return match.group(1)
