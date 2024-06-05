# fmlib

Common python libraries used across projects.

## Integration

To integrate it into a new project, 

1. Add `fmlib` into your project as a git submodule

    ```shell
    git submodule add git@github.com:fairmatic/fmlib.git fmlib
    ```
    This will create a new folder `fmlib` in your project, and will also create a `.gitmodules` file. 


2. Add the following line in the project's `requirements.txt` file to include fmlib's dependencies.

    ```
    -r ./fmlib/requirements.txt
    ```

3. Now fmlib modules can be imported and used in your project.

    ```shell
    from fmlib.scheduler import ScheduledJobRunner

    job_runner = ScheduledJobRunner(
            jobs=JOBS
        )
    ```