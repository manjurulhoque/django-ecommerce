import graphene

from .types import ExpectedErrorType


class Output:
    """
        A class to all public classes extend to patronize the output
    """

    success = graphene.Boolean(default_value=True)
    errors = graphene.Field(ExpectedErrorType)
