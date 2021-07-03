# -*- coding: utf-8 -*-

import pytest


def pytest_addoption(parser):
    group = parser.getgroup('fold')
    group.addoption(
        '--foo',
        action='store',
        dest='dest_foo',
        default='2021',
        help='Fold reults in console'
    )

    parser.addini('HELLO', 'Dummy pytest.ini setting')


@pytest.fixture
def bar(request):
    return request.config.option.dest_foo
