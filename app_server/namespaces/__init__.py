from flask_restx import Api as BaseAPI


class Api(BaseAPI):
    def _register_doc(self, app_or_blueprint):
        # HINT: This is just a copy of the original implementation with the last line commented out.
        if self._add_specs and self._doc:
            # Register documentation before root if enabled
            app_or_blueprint.add_url_rule(self._doc, "doc", self.render_doc)

    @property
    def base_path(self):
        return ""


alchemiser_api = Api(
    title="Achemiser API SERVER",
    version="1.0",
    description="REST APIs for Alchemiser",
)


def init_namespaces():
    # Import and register namespaces here
    from app_server.namespaces.health import health_check_namespace

    alchemiser_api.add_namespace(health_check_namespace, path="/health")
