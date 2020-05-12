import re


class QuestionnaireMixins:
    client = None
    csrf_token = None

    def get(self, url, name=None, expect_redirect=False):
        with self.client.get(
            url=url, name=name, allow_redirects=False, catch_response=True
        ) as response:

            if expect_redirect:
                if response.status_code != 302:
                    error = f"Expected a (302) but got a ({response.status_code}) back when getting page: {url}"
                    response.failure(error)
                    raise Exception(error)
                return response

            if response.status_code != 200:
                error = f"Expected a (200) but got a ({response.status_code}) back when getting page: {url}"
                response.failure(error)
                raise Exception(error)

            if not response.content:
                response.failure(f"No content in GET response for url: {url}")

            self.csrf_token = _extract_csrf_token(response.content.decode('utf8'))

            return response

    def post(self, base_url, request_url, data={}, name=None):

        data['csrf_token'] = self.csrf_token
        headers = {'Referer': base_url}

        with self.client.post(
            allow_redirects=False,
            headers=headers,
            data=data,
            url=request_url,
            name=name,
            catch_response=True,
        ) as response:

            if response.status_code != 302:
                error = f"Expected a (302) but got a ({response.status_code}) back when posting page: {request_url} with data: {data}"
                response.failure(error)
                raise Exception(error)

            return response


CSRF_REGEX = re.compile(
    r'<input id="csrf_token" name="csrf_token" type="hidden" value="(.+?)">'
)


def _extract_csrf_token(html):
    match = CSRF_REGEX.search(html)
    if match:
        return match.group(1)
