Flake8 Restrict Imports Plugin
==============================

Overview
--------

This Flake8 plugin provides a mechanism to restrict imports based on a specified configuration. The plugin allows you to define sets of denied and allowed imports, helping you enforce coding standards and maintain a clean codebase.

### Features

-   Denied Imports: Specify a configuration that defines imports to be denied for specific modules/packages.
-   Allowed Imports: Specify a configuration that defines allowed imports for specific modules/packages.

Installation
------------

Install the plugin using `pip`:


`pip install flake8-restrict-imports`

Usage
-----

Once the plugin is installed, you can run Flake8 with the plugin enabled:


`flake8 your_project_directory`

### Configuration

You need to configure the plugin in your Flake8 configuration file (e.g., `.flake8`):


```[flake8]
denied_imports_config = {'libs': ['db', 'tests'],'db': ['libs', 'tests']}
allowed_imports_config = {'api.tests.utils': ['db', 'libs'], 'db': ['tests']}
```

Adjust the configurations based on your project's needs.

### Example

Consider the following code snippet:


```
# your_module.py

# Denied import
from core import some_module  # This import is denied according to the configuration

# Allowed import
from api.tests.event_utils import some_function  # This import is allowed according to the configuration
```

# Denied import
`from core import some_module` This import is denied according to the configuration

# Allowed import
`from api.tests.event_utils import some_function` This import is allowed according to the configuration`

When Flake8 is run, it will raise a warning for the denied import and ensure compliance with your defined import restrictions.

Contribution
------------

Feel free to contribute to the development of this Flake8 plugin. Fork the repository, make your changes, and submit a pull request.

License
-------

This Flake8 plugin is licensed under the MIT License.