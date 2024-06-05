# SERVICENAME

## Initial Step
Replace the `SERVICENAME` string with your service name in all the folders and files.
- Command for Mac to replace in all the files:
```
 LC_ALL=C find . -type f   -exec sed -i '' s/SERVICENAME/<YOUR_SERVICE_NAME>/g {} +
```
```
eg. LC_ALL=C find . -type f   -exec sed -i '' s/SERVICENAME/dummy_service/g {} +
```
- Rename `SERVICENAME` Folder in `dockerfiles` to `<YOUR_SERVICE_NAME>`

## Local Setup
- Install Python v3.9
    - Cmd for Mac
    ```
    brew install python@3.9
    ```

- Create virtual environment and activate it
```
 python3.9 -m venv SERVICENAME_ENV
 source SERVICENAME_ENV/bin/activate
```

- Add and Update the git modules
```
 git submodule update --init --recursive
```

- Install dependencies
```
 pip install -r requirements.txt
```

- Setup environment variables
```
 export FM_ENV=dev
 export FLASK_APP=app.py
```

- Creating the tables in DB for the first time
`Note: Make sure you have the database running`
```
 cd dockerfiles/SERVICENAME/test/
 docker-compose up --detach
```
```
 python -m flask db init
 python -m flask db migrate
 python -m flask db upgrade
```
- For migrating the database schema changes (after the first time), `db init` command is not needed
```
 python -m flask db migrate
 python -m flask db upgrade
```

- Run the application
```
 python -m flask run
```

- Testing the service
```
 curl http://localhost:5000/health
```

### Contributing
- Install dependencies for Pre-commit
```
 pip install -r requirements-dev.txt
```
- To install pre-commit hooks
```
 pre-commit install
 pre-commit install-hooks
```

## Running unit tests
- Install pytest
```
 pip install pytest # If not present.
```
- Spin up the test Database
```
 cd dockerfiles/SERVICENAME/test/
 docker-compose up --detach
```
- Run the tests after moving to the root directory
```
 cd <Working Dir>/SERVICENAME
 export PYTHONPATH=.
 FM_ENV=test pytest app_server
```

## Documentation

[Product Document]()


## Steps to Onboard a Service
[Onboarding Checklist](https://fairmatic.atlassian.net/wiki/spaces/EN/pages/235503671/Service+onboarding+checklist)
