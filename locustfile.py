import os

from locust import HttpLocust

from runner_benchmark.taskset import SurveyRunnerTaskSet


class SurveyRunnerScenario(HttpLocust):
    task_set = SurveyRunnerTaskSet
    host = os.getenv("HOST", "http://localhost:5000")
