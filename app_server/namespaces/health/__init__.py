import json

from flask_restx import Namespace, Resource
from healthcheck import EnvironmentDump, HealthCheck

from app_server.db import check_connection

health_check_namespace = Namespace(
    "health-check",
    description="API Namespace for Fairmatic Insurance Products",
)

health = HealthCheck()
envdump = EnvironmentDump()


def db_check():
    return check_connection(), "DB connection is available"


health.add_check(db_check)


@health_check_namespace.route("")
class Health(Resource):
    def get(self):
        """
        Returns a JSON response for the health check endpoint.

        :return: JSON response with the key "status_code.
        :rtype: dict
        """
        health_status = health.check()

        return json.loads(health_status[0]), health_status[1]
