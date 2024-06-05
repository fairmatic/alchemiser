import time
from typing import List, TYPE_CHECKING

from .scheduler import JobScheduler

if TYPE_CHECKING:
    from . import BaseTask


class ScheduledJobRunner:
    TIME_BETWEEN_RUNS = 60.0

    def __init__(self, jobs: List['BaseTask']):
        self.jobs = jobs
        self.job_scheduler = JobScheduler()
        self.schedule_job()

    def schedule_job(self):
        for health_check in self.jobs:
            self.job_scheduler.schedule_job(
                health_check.run_task,
                health_check.repeat_interval,
                health_check.interval_type
            )

    def run(self):
        while True:
            start_time = time.time()
            self.job_scheduler.scheduler.run_pending()
            end_time = time.time()
            remaining_time = max(self.TIME_BETWEEN_RUNS - end_time + start_time, 0)
            time.sleep(remaining_time)
