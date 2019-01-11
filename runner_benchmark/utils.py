import os
import random
import re
import time

r = random.Random()

collection_exercise_sid_regex = re.compile('\/[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12}\/', re.I)
eq_id_form_type_regex = re.compile(r'questionnaire/([^/]*)/([^/]*)/')

class QuestionnaireMixins:
    client = None
    csrftoken = None
    prevurl = None

    def get(self, *args, **kwargs):
        allow_redirects = kwargs.pop('allow_redirects', False)
        kwargs.pop('method', None)

        response = self.client.get(allow_redirects=allow_redirects, *args, **kwargs)

        if not response.content:
            raise Exception(f"No content in GET response for url: {kwargs['url']}")

        self.csrftoken = _extract_csrf_token(response.content.decode('utf8'))
        return response

    def post(self, *args, **kwargs):
        data = kwargs.pop('data', {}) or {}
        kwargs.pop('method', None)
        allow_redirects = kwargs.pop('allow_redirects', False)

        data['csrf_token'] = self.csrftoken

        headers = {
            'Referer': self.prevurl
        }

        response = self.client.post(allow_redirects=allow_redirects, headers=headers, data=data, *args, **kwargs)
        return response


CSRF_REGEX = re.compile(r'<input id="csrf_token" name="csrf_token" type="hidden" value="(.+?)"/>')
def _extract_csrf_token(html):
    match = CSRF_REGEX.search(html)
    if match:
        return match.group(1)


GROUP_INSTANCE_REGEX = re.compile(r'/questionnaire/[^/]*/[^/]*/[\w-]+/[\w-]+/(\d)+/[\w-]+')
def _extract_group_instance(url):
    match = GROUP_INSTANCE_REGEX.search(url)
    if match:
        return match.group(1)

def replace_collection_exercise_sid(url, new_sid):
    return collection_exercise_sid_regex.sub('/{}/'.format(new_sid), url)

def get_questionnaire_from_request(request):
    """
    Extract the EQ_ID and form_type from a request to survey runner
    """
    matches = eq_id_form_type_regex.search(request['url'])
    return matches.group(1, 2)
