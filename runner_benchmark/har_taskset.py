import os
import time
import random
from pathlib import Path
from locust import TaskSet, task
import utils
from har_parser import parse_har_file
from token_generator import create_token
from urllib.parse import urlsplit
from uuid import uuid4

r = random.Random()

class HarFileTaskSet(TaskSet, utils.QuestionnaireMixins):
    def __init__(self, parent):
        super().__init__(parent)

        self.base_url = self.locust.client.base_url

        self.har_filepath = os.environ.get('HAR_FILEPATH', 'requests.har')
        self.eq_id = os.environ.get('EQ_ID')
        self.form_type_id = os.environ.get('FORM_TYPE')

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

                if response.status_code != 200:
                    raise Exception(f"Got a non-200 ({response.status_code}) back when getting page: {request['url']}")

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

        token = create_token(
            form_type_id=self.form_type_id,
            eq_id=self.eq_id,
            region_code='GB-ENG',
            country='E',
            address_line1='68 Abingdon Road',
            address_line2='Some place',
            locality='Some locale',
            town_name='Some town',
            display_address='68 Abingdon Road, Some place, PE12 4GH',
            postcode='PE12 4GH',
            roles=[],
            variant_flags={'sexual_identity': 'false'},
            collection_exercise_sid=str(uuid4())
        )

        url = f'/session?token={token}'
        response = self.get(url=url, name="/session")

        if response.status_code != 302:
            raise Exception('Got a non-302 back when authenticating session: {}'.format(response.status_code))

        return self.get(url=response.headers['Location'])
