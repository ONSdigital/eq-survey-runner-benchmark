import os

from locust import constant, HttpUser

from runner_benchmark.taskset import SurveyRunnerTaskSet


class SurveyRunnerScenario(HttpUser):
    wait_time = constant(0)
    tasks = [SurveyRunnerTaskSet]
    host = os.getenv("HOST", "http://localhost:5000")
