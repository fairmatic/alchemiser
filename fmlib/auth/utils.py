from supertokens_python.recipe.session.framework.flask import verify_session
from supertokens_python.recipe.userroles import UserRoleClaim, PermissionClaim

def get_verification_lambda(role, permission):
    return (
        lambda global_validators, session, user_context: global_validators
        + [UserRoleClaim.validators.includes(role)]
        + [PermissionClaim.validators.includes(permission)]
    )


def verify_session_decorator(role, permission):
    return verify_session(
        override_global_claim_validators=get_verification_lambda(role, permission)
    )