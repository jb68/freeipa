#
# Copyright (C) 2016  FreeIPA Contributors see COPYING for license
#
from __future__ import print_function

import os
import pprint
import sys

import pytest

from ipalib import api
from ipalib.cli import cli_plugins

try:
    import ipaplatform  # pylint: disable=unused-import
except ImportError:
    ipaplatform = None
try:
    import ipaserver
except ImportError:
    ipaserver = None

HERE = os.path.dirname(os.path.abspath(__file__))

pytest_plugins = [
    'ipatests.pytest_plugins.additional_config',
    'ipatests.pytest_plugins.beakerlib',
    'ipatests.pytest_plugins.declarative',
    'ipatests.pytest_plugins.nose_compat',
]
# The integration plugin is not available in client-only builds.
if ipaserver is not None:
    pytest_plugins.append('ipatests.pytest_plugins.integration')


MARKERS = [
    'tier0: basic unit tests and critical functionality',
    'tier1: functional API tests',
    'cs_acceptance: Acceptance test suite for Dogtag Certificate Server',
    'ds_acceptance: Acceptance test suite for 389 Directory Server',
    'skip_ipaclient_unittest: Skip in ipaclient unittest mode',
]


NO_RECURSE_DIRS = [
    # build directories
    'ipaclient/build',
    'ipalib/build',
    'ipaplatform/build',
    'ipapython/build',
    'ipaserver/build',
    'ipatests/build',
    # install/share/wsgi.py
    'install/share'
]


INIVALUES = {
    'python_classes': ['test_', 'Test'],
    'python_files': ['test_*.py'],
    'python_functions': ['test_*'],
}


def pytest_configure(config):
    # add pytest markers
    for marker in MARKERS:
        config.addinivalue_line('markers', marker)

    # do not recurse into build directories or install/share directory.
    for norecursedir in NO_RECURSE_DIRS:
        config.addinivalue_line('norecursedirs', norecursedir)

    # addinivalue_line() adds duplicated entries and does not remove existing.
    for name, values in INIVALUES.items():
        current = config.getini(name)
        current[:] = values

    # set default JUnit prefix
    if config.option.junitprefix is None:
        config.option.junitprefix = 'ipa'

    # always run doc tests
    config.option.doctestmodules = True


def pytest_addoption(parser):
    group = parser.getgroup("IPA integration tests")
    group.addoption(
        '--ipaclient-unittests',
        help='Run ipaclient unit tests only (no RPC and ipaserver)',
        action='store_true'
    )


def pytest_cmdline_main(config):
    api.bootstrap(
        context=u'cli', in_server=False, in_tree=True, fallback=False
    )
    for klass in cli_plugins:
        api.add_plugin(klass)

    # XXX workaround until https://fedorahosted.org/freeipa/ticket/6408 has
    # been resolved.
    if ipaserver is not None:
        api.finalize()

    if config.option.verbose:
        print('api.env: ')
        pprint.pprint({k: api.env[k] for k in api.env})
        print("uname: {}".format(os.uname()))
        print("euid: {}, egid: {}".format(os.geteuid(), os.getegid()))
        print("working dir: {}".format(os.path.abspath(os.getcwd())))
        print('sys.version: {}'.format(sys.version))


def pytest_runtest_setup(item):
    if isinstance(item, item.Function):
        if item.get_marker('skip_ipaclient_unittest'):
            # pylint: disable=no-member
            if pytest.config.option.ipaclient_unittests:
                pytest.skip("Skip in ipaclient unittest mode")
