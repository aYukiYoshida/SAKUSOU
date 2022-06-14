# -*- coding: utf-8 -*-

import pytest
from saku import __version__


@pytest.mark.app
def test_version():
    assert __version__ == '0.1.0'
