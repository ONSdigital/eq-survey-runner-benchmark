from locust import HttpLocust

from har_taskset import HarFileTaskSet

class SurveyRunnerSimpleScenario(HttpLocust):
    task_set = HarFileTaskSet
