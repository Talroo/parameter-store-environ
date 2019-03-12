import os
import unittest

from ps_environ.environ import Env

from botocore.stub import Stubber
import boto3

class BaseTests(unittest.TestCase):
    def setUp(self):
        self.env = Env(service='test-service', stage='dev')

    def test_local_env_var_overrides(self):
        pass

    def test_raise_improperly_configured(self):
        """ Test that the ImproperlyConfigured Exception is raised if variable is missing """
        pass

class CastTests(unittest.TestCase):
    def setUp(self):
        self.env = Env(service='test-service', stage='dev')

    def test_casting_collections(self):
        pass

    def test_casting_json(self):
        pass

    def test_bad_cast_raises_exception(self):
        pass

    def test_get_cast_from_schema(self):
        pass