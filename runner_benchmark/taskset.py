import json
import os
import random
import re
import time

from locust import TaskSet, task

from .questionnaire_mixins import QuestionnaireMixins
from .token_generator import create_token
from .utils import parse_params_from_location

r = random.Random()


class SurveyRunnerTaskSet(TaskSet, QuestionnaireMixins):
    def __init__(self, parent):
        super().__init__(parent)

        self.base_url = self.client.base_url
        self.redirect_params = {}
        self.include_schema_url_in_token = (
            os.getenv("INCLUDE_SCHEMA_URL_IN_TOKEN", "false").lower() == "true"
        )

        requests_filepath = os.environ.get("REQUESTS_JSON", "requests.json")

        with open(requests_filepath, encoding="utf-8") as requests_file:
            requests_json = json.load(requests_file)
            self.schema_name = requests_json["schema_name"]
            self.requests = requests_json["requests"]
            self.schema_url = requests_json["schema_url"]

    @task
    def start(self):
        self.do_launch_survey()
        self.replay_requests()

    def replay_requests(self):
        user_wait_time_min = int(os.getenv("USER_WAIT_TIME_MIN_SECONDS", 1))
        user_wait_time_max = int(os.getenv("USER_WAIT_TIME_MAX_SECONDS", 2))
        url_name_regex = r"{.*?}"

        self.get("/questionnaire", expect_redirect=True)

        for request in self.requests:
            url_name = re.sub(url_name_regex, "{id}", request["url"])
            request_url = request["url"].format_map(self.redirect_params)

            if request["method"] == "GET":
                expect_redirect = "redirect_route" in request
                response = self.get(
                    request_url, name=url_name, expect_redirect=expect_redirect
                )

                if expect_redirect:
                    self.handle_redirect(request, response)

                if user_wait_time_min and user_wait_time_max:
                    time.sleep(r.randint(user_wait_time_min, user_wait_time_max))

            elif request["method"] == "POST":
                response = self.post(
                    self.base_url, request_url, request["data"], name=url_name
                )
                if "redirect_route" in request:
                    self.handle_redirect(request, response)

            else:
                raise Exception(
                    f"Invalid request method {request['method']} for request to: {request_url}"
                )

    def handle_redirect(self, request, response):
        self.redirect_params.update(
            parse_params_from_location(
                response.headers["Location"], request["redirect_route"]
            )
        )

    def do_launch_survey(self):
        extra_payload = (
            dict(schema_url=self.schema_url) if self.include_schema_url_in_token else {}
        )
        token = create_token(schema_name=self.schema_name, **extra_payload)

        url = f"/session?token={token}"
        self.get(url=url, name="/session", expect_redirect=True)
