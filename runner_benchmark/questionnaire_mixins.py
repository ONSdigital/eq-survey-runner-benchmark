import re


class QuestionnaireMixins:
    client = None
    csrf_token = None

    def get(self, url, allow_redirects=False, name=None):
        response = self.client.get(allow_redirects=allow_redirects, url=url, name=name)

        if not response.content:
            raise Exception(f"No content in GET response for url: {url}")

        if response.status_code != 302:
            self.csrf_token = _extract_csrf_token(response.content.decode('utf8'))

        return response

    def post(self, base_url, request_url, data={}, name=None):

        data['csrf_token'] = self.csrf_token

        headers = {'Referer': base_url}

        response = self.client.post(
            allow_redirects=False, headers=headers, data=data, url=request_url, name=name
        )
        return response


CSRF_REGEX = re.compile(
    r'<input id="csrf_token" name="csrf_token" type="hidden" value="(.+?)">'
)


def _extract_csrf_token(html):
    match = CSRF_REGEX.search(html)
    if match:
        return match.group(1)
