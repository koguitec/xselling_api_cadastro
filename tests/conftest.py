"""Test module automatically loaded by pytest"""
# pylint: disable=w0621
from typing import Dict

import pytest

from application.app import create_app
from manage import read_json_configuration


@pytest.fixture
def app():
    """Factory for application

    Returns:
        Object: Application configuration
    """
    app = create_app('testing')

    return app


def pytest_addoption(parser):
    """Hook into the pytest CLI parser that adds the option --integration
    When the 'integration' option is specified on the command line the pytest
    setup will contain the key integration with value True

    Args:
        parser (Object): Pytest CLI parser object
    """
    parser.addoption(
        '--integration', action='store_true', help='run integrations tests'
    )


def pytest_runtest_setup(item):
    """Hook into the pytest setup of every single test
    The attribute item.config contains the parsed pytest command line.

    If the test is marked with integration ('integration' in item.keywords) and
    the option --integration is not present (not item.config.getvalue("integration"))
    the test is skipped.

    Args:
        item (Object): Pytest CLI item object
    """
    if 'integration' in item.keywords and not item.config.getvalue(
        'integration'
    ):
        pytest.skip('need --integration option to run')


@pytest.fixture(scope='session')
def app_configuration() -> Dict:
    """Loads database configuration to connect during tests.
    Options: "testing", "production"

    The name of the configuration is hardcoded for simplicity's sake. Another
    solution might be to create an environment variable with the application
    configuration in the management script and read it from there.

    Returns:
        Dict: Key, value configuration params
    """
    return read_json_configuration('testing')
