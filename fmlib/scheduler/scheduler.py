import threading
from typing import Callable

import schedule

from .check import IntervalType


class JobScheduler:
    def __init__(self):
        self.scheduler = schedule.default_scheduler

    def cancel_job(self, job_fn) -> None:
        return self.scheduler.cancel_job(job_fn)

    @staticmethod
    def run_job_thread(job_fn: Callable):
        thread = threading.Thread(target=job_fn)
        thread.start()

    def schedule_job(
            self,
            job_fn: Callable,
            interval: int,
            interval_type: IntervalType
    ) -> None:
        getattr(self.scheduler.every(interval=interval), interval_type.value).do(self.run_job_thread, job_fn)
