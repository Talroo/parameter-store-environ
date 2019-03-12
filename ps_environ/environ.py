from functools import partialmethod
from typing import Any, Collection, Dict, Optional
import json
import os

import boto3


class ImproperlyConfigured(Exception):
    pass


class NOTSET:
    # We use this as the default instead of None since None can be a valid default value
    pass


class Env:
    """
    Grab variables from AWS Parameter Store or local environment

    Usage:::

        >>> env = Env(service='test-service', stage='dev')
        >>> env('FOO')
        'bar'
        >>> env('DEBUG')
        'True'
        >>> env.bool('DEBUG')
        True

        # Supports passing in a schema to avoid having to always call the casting methods
        >>> env = Env(service='test-service', stage='dev', schema={'MAIL_ENABLED': bool, 'MAX_RETRIES': int})
        >>> env('MAIL_ENABLED')
        True
        >>> env('MAX_RETIRES')
        5
    """

    BOOLEAN_TRUE_STRINGS = ('true', 't', 'yes', 'y', '1')

    def __init__(
        self,
        service: str,
        stage: str,
        schema: Optional[Dict[str, Any]] = None,
    ):
        self.service = service
        self.stage = stage
        self.schema = schema or {}
        self.parameter_store_cache = {}

        self.ssm = boto3.client('ssm')
        self._init_parameter_store_cache()

    def __call__(self, var: str, cast: Any = None, default: Any = NOTSET):
        """
        Return given variable

        :param var: Variable name to get
        :param default: Default value to return
        :param cast: Type or callable to cast return value as

        :returns: Value from Parameter Store/Environment if set
        """
        item = os.environ.get(var) or self.parameter_store_cache.get(var)
        if item is None:
            if default is NOTSET:
                raise ImproperlyConfigured(f'Variable {var} not found in either parameter store or environment.')
            item = default

        # If a cast type was passed in use that, else check the schema
        cast = cast or self.schema.get(var)
        return self.cast(item, cast) if cast else item

    def _init_parameter_store_cache(self):
        # TODO: Decide if we should just let any except from boto bubble up
        # or keep on swallowing them and maybe just log a warning?
        parameters = self.ssm.get_parameters_by_path(
            Path=f'/{self.service}/{self.stage}',
            WithDecryption=True,
        )['Parameters']
        self.parameter_store_cache = {
            param['Name'].split('/')[-1]: param['Value'] for param in parameters
        }

    def refresh(self):
        """
        Refresh the cache from Parameter Store
        """
        self._init_parameter_store_cache()

    @classmethod
    def cast(cls, value, cast=str):
        """
        Grab given variable and cast is as given type
    
        :param value: Value to cast
        :param cast: Type or callable to cast return value as
        
        :returns: Casted value
        """

        if cast is bool:
            return value.lower() in cls.BOOLEAN_TRUE_STRINGS

        if issubclass(cast, Collection):
            # Create a generator for the cast method to use
            value = (v.strip() for v in value.split(','))

        try:
            return cast(value)
        except ValueError as error:
            raise ImproperlyConfigured(*error.args)

    bool = partialmethod(__call__, cast=bool)
    float = partialmethod(__call__, cast=float)
    int = partialmethod(__call__, cast=int)
    set = partialmethod(__call__, cast=set)
    list = partialmethod(__call__, cast=list)
    tuple = partialmethod(__call__, cast=tuple)
    json = partialmethod(__call__, cast=json.loads)
