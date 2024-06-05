# Job Scheduling

In order to create a scheduled job to perform some task at given interval, do the following:


1. Create all the jobs that you would like to have scheduled by the scheduler.

    ```python
    from fmlib.scheduler import BaseTask, IntervalType
    
    
    class SampleTask(BaseTask):
        repeat_interval = 15
        interval_type = IntervalType.minutes
    
        @classmethod
        def run(cls):
            # logic that needs to be scheduled
            ...
    ```

2. Gather all jobs that need to be scheduled by the scheduler

    ```python
    all_jobs = [
        SampleTask,
        AnotherSampleTask,
        ...
    ]
    ```
   
3. Create the scheduler for the above metrics and run it

    ```python
    from fmlib.scheduler import ScheduledJobRunner
    
    job_runner = ScheduledJobRunner(
        jobs=all_jobs
    )
    
    job_runner.run()
    ```
