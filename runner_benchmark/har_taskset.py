import os
import random
import time
from pathlib import Path
from urllib.parse import urlsplit

from locust import TaskSet, task

import utils
from har_parser import parse_har_file
from token_generator import create_token

r = random.Random()


class HarFileTaskSet(TaskSet, utils.QuestionnaireMixins):
    def __init__(self, parent):
        super().__init__(parent)

        self.base_url = self.locust.client.base_url

        self.har_filepath = os.environ.get('HAR_FILEPATH', 'requests.har')
        self.schema_name = os.environ.get('SCHEMA_NAME')

        self.parse_har_file()

    def parse_har_file(self):
        filepath = Path(self.har_filepath)
        absolute_path = filepath.absolute()
        self.requests = parse_har_file(absolute_path)

    @task
    def start(self):
        self.do_launch_survey()
        self.replay_requests()

    def replay_requests(self):
        user_wait_time_min = int(os.getenv('USER_WAIT_TIME_MIN_SECONDS', 0))
        user_wait_time_max = int(os.getenv('USER_WAIT_TIME_MAX_SECONDS', 0))

        for request in self.requests:
            request_base_url = "{0.scheme}://{0.netloc}".format(urlsplit(request['url']))
            request['url'] = request['url'].replace(request_base_url, self.base_url)

            if request['method'] == 'GET':
                response = self.get(**request)

                if response.status_code not in [200, 302]:
                    raise Exception(
                        f"Got a ({response.status_code}) back when getting page: {request['url']}"
                    )

                print("Waiting after GET request")

                if user_wait_time_min and user_wait_time_max:
                    time.sleep(r.randrange(user_wait_time_min, user_wait_time_max))
            elif request['method'] == 'POST':

                print('POST to ', request['url'])

                response = self.post(**request)

                if response.status_code != 302:
                    raise Exception(f"Got a non-302 ({response.status_code}) back when posting page: {request['url']} with data: {request['data']}")

                print(f"Redirect to: {response.headers['Location']}")

            else:
                raise Exception(f"Invalid request method {request['method']} for request to: {request['url']}")

    def do_launch_survey(self):

        token = create_token(schema_name=self.schema_name)

        url = f'/session?token={token}'
        response = self.get(url=url, name='/session')

        if response.status_code != 302:
            raise Exception('Got a non-302 back when authenticating session: {}'.format(response.status_code))

        return self.get(url=response.headers['Location'])
