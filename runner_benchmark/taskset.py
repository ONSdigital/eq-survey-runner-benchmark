import json
import os
import random
import time

from locust import TaskSet, task

from .utils import parse_params_from_location, has_params
from .questionnaire_mixins import QuestionnaireMixins
from .token_generator import create_token

r = random.Random()


class SurveyRunnerTaskSet(TaskSet, QuestionnaireMixins):
    def __init__(self, parent):
        super().__init__(parent)

        self.base_url = self.locust.client.base_url

        requests_filepath = os.environ.get('REQUESTS_JSON', 'requests.json')

        with open(requests_filepath, encoding='utf-8') as requests_file:
            requests_json = json.load(requests_file)
            self.schema_name = requests_json['schema_name']
            self.requests = requests_json['requests']

    @task
    def start(self):
        self.do_launch_survey()
        self.replay_requests()

    def replay_requests(self):
        user_wait_time_min = int(os.getenv('USER_WAIT_TIME_MIN_SECONDS', 0))
        user_wait_time_max = int(os.getenv('USER_WAIT_TIME_MAX_SECONDS', 0))

        redirect_params = {}

        for request in self.requests:
            request_url = request['url'].format(**redirect_params) if has_params(request['url']) else request['url']

            if request['method'] == 'GET':
                response = self.get(request_url)

                if response.status_code not in [200, 302]:
                    raise Exception(
                        f"Got a ({response.status_code}) back when getting page: {request_url}"
                    )
                if response.status_code == 302:
                    print(f"Redirect location: {response.headers['Location']}")
                    if 'param_url' in request:
                        redirect_params = parse_params_from_location(response.headers['Location'], request['param_url'])

                if user_wait_time_min and user_wait_time_max:
                    print("Waiting after GET request")
                    time.sleep(r.randrange(user_wait_time_min, user_wait_time_max))

            elif request['method'] == 'POST':
                print('POST to ', request_url)

                response = self.post(self.base_url, request_url, request['data'])

                if response.status_code not in [200, 302]:
                    raise Exception(
                        f"Got a ({response.status_code}) back when posting page: {request_url} with data: {request['data']}"
                    )
                if response.status_code == 302:
                    print(f"Redirect location: {response.headers['Location']}")
                    if 'param_url' in request:
                        redirect_params = parse_params_from_location(response.headers['Location'], request['param_url'])

            else:
                raise Exception(
                    f"Invalid request method {request['method']} for request to: {request_url}"
                )

    def do_launch_survey(self):

        token = create_token(schema_name=self.schema_name)

        url = f'/session?token={token}'
        response = self.get(url)

        if response.status_code != 302:
            raise Exception(
                'Got a non-302 back when authenticating session: {}'.format(
                    response.status_code
                )
            )

        self.get(response.headers['Location'], allow_redirects=True)
