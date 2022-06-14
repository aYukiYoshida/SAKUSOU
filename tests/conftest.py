# -*- coding: utf-8 -*-

import pytest

def pytest_addoption(parser):
    '''
    parse command line option
    '''
    parser.addoption(
        '--app',
        action='store_true',
        default=False,
        help='run testing for ATTA application.'
    )

    parser.addoption(
        '--api',
        action='store_true',
        default=False,
        help='run testing for web api.'
    )

def pytest_collection_modifyitems(session, config, items):
    for mark in ('app', 'api'):
        option = '--' + mark
        if not config.getoption(option):
            skip_testing = pytest.mark.skip(
                reason=f'The option of {option} is required to run.')

            for item in items:
                if mark in item.keywords:
                    item.add_marker(skip_testing)
