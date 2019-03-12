# ps-environ

## Description
This is a simple wrapper around AWS SSM Parameter Store. It is designed to cache and parse variables from Parameter Store for a specific service and stage.
It is heavily inspired by [django-environ](https://github.com/joke2k/django-environ) and shares a (simplified) interface.

For more on Parameter Store, read the [AWS documentation](https://docs.aws.amazon.com/systems-manager/latest/userguide/systems-manager-paramstore.html).

## Installation

Install with `pip`:

``` bash
pip install parameter-store-environ 
```

## Usage
The wrapper assumes that variables in parameter store are in the following format:
`/<SERVICE>/<STAGE>/<VARIABLE_NAME>`

So, for example:
```
/api/dev/DEBUG
/api/prod/DB_HOST
```

The wrapper is agnostic to the variable name, but we recommend you follow the convention for environment variables and use all caps and underscores. 

In your settings/configuration module, import the module and create a new instance of the wrapper

``` python
from ps_environ import Env
config = Env(service='api', stage='dev')

# When called directly, the string value is returned
assert config('DEBUG') == 'True'

# Use casting methods to return the type you need
assert config.bool('DEBUG') == True
```

### Schemas
You can define a schema when you instantiate the wrapper to avoid having to call the casting methods
``` python
config = Env(service='api', stage='dev', schema={
    'DEBUG': bool,
    'MAX_RETRIES': int,
})

assert config('DEBUG') == True
assert config('MAX_RETRIES') == 5
```

Supported casting types: bool, float, int, set, list, tuple, json

Additional Notes:

* `list, tuple, set`: These types expect the values to be separated by commas. E.g. `1,2,3`
* `json`: A regular JSON string is expected. E.g. `{'foo': 'bar'}`

### Environment Variable Override
If the variable is also set in the environment, that value will take precedence. 

### Default Values
You can set a default value by setting the default keyword.
If no default is set and the value is neither in the environment variables or in parameter store, an `ImproperlyConfigured` exception will be raised.
``` python
assert config('DB_HOST', default='localhost') == 'localhost'
```

## AWS Credentials
`ps-environ` uses `boto3` to interface with parameter store and therefore uses the same mechanism for authentication.
See the [configuring credentials](https://boto3.readthedocs.io/en/latest/guide/configuration.html#configuring-credentials) in the Boto 3 documentation for more information.
