import os

from locust import HttpLocust

from har_taskset import HarFileTaskSet


class SurveyRunnerSimpleScenario(HttpLocust):
    task_set = HarFileTaskSet
    host = os.getenv("HOST", "http://localhost:5000")


if __name__ == "__main__":
    SurveyRunnerSimpleScenario().run()
