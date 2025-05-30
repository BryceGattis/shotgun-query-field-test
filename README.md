# shotgun-query-field-test
A test to obtain the value of query fields in Shotgun/ShotGrid/Flow and display the result in a HTML table.

## Using the library

## Dependencies

This package uses the Python package [Keyring](https://pypi.org/project/keyring/).
Therefore, prior to using the library, you must first set up the following credentials in your system's keyring service:

```commandline
shotgun.api.url - The URL to the Shotgun site.
shotgun.api.script_name - The API script's name.
shotgun.api.api_key - The API script's API Key.
```

Otherwise, you will get an EnvironmentError when the program initially attempts to create a SG connection.

## Development

### Dependencies

We are using GNU Make to simplify common commands for this repo. This will not be pre-installed on Windows.
I recommend installing it with `winget`.

### Virtual Environment

For development, I recommend a virtual environment by running the following command:

```commandline
python -m venv venv
```

Next we'll need to activate the environment in your current shell by running the following:

```commandline
Windows: venv/Scripts/activate.bat
MacOS/Linux: source venv/bin/activate
```

Lastly, we will install this package (and its dependencies) to the virtual environment:

```commandline
python -m pip install .
```

### IDE

Lastly, we need to ensure that our IDE is aware of the virtual environment and can use it for
auto-complete, type-hinting etc.

In Pycharm, in the top menu, go to File->Settings which will open a new pop-up window. In the pop-up
window, go to Project->Python Interpreter and change the configuration to use your newly created
virtual environment.

## Testing

To run the associated unit tests, you will need to install the package with the `[test]` dependency
specified like so:

```commandline
python -m pip install .[test]
```