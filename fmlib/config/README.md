# Configuration Management

Library to handle configuration across various environments (prod, dev, etc)

## Fundamentals

1. Config should be in `settings.toml` file in the project root
2. Config file supports multiple environments like prod, dev, etc
3. Config file supports default values

```toml
[default]
port = 80
user = ""

[test]
port = 7050
user = "test"

[prod]
port = 80
user = "admin"
```

## Accessing Config Items in Python

```python
# config.py is at project root. Import accordingly
from config import settings

start_http_server(settings.host, settings.port)
```

## Changing Environment

Environment used by the library can be changed by setting the `FM_ENV` environment variable.

```shell
export FM_ENV=prod
# Run your app now
```

## Override config with ENV variables
1. Individual config items can be overridden using ENV variables. If the setting name is `xyz` then the ENV variable to update is `FM_XYZ`. `FM_` is the common prefix.
2. ENV variables take precedence over config file
3. [Do] Use this during local testing for quickly changing config
4. [Do] Use this in production to sync secrets from vault to ENV variables
5. [Don't] Use this as an alternative config source

## Managing Secrets
1. For local testing, use `settings.toml` file
2. Don't store production secrets in `settings.toml` or code
3. For production + ECS setup, use AWS SecretManager and sync to ENV variables. This sync is supported via ansible config. Reach out to SRE team for further info
4. For production + Lambda setup, reach out to SRE team for further info

## Initializing Config Setup for new projects

Make sure fmlib is added as submodule to your project git repo. Details [here](https://github.com/fairmatic/fmlib)

Once fmlib is added as submodule, run the following command from project root.
```shell
cp fmlib/config/sample/* .
```


## More information and troubleshooting
We use [dynaconf](https://www.dynaconf.com/) and their documentation is good. Please refer to their website for more info.
