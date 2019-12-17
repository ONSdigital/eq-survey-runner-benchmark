import os

from locust.contrib.fasthttp import FastHttpLocust

from runner_benchmark.taskset import SurveyRunnerTaskSet


class SurveyRunnerScenario(FastHttpLocust):
    task_set = SurveyRunnerTaskSet
    host = os.getenv("HOST", "http://localhost:5000")
