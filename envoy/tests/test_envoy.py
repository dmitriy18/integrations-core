# (C) Datadog, Inc. 2018-present
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)
from copy import deepcopy

import mock
import pytest
import requests

from datadog_checks.envoy import Envoy
from datadog_checks.envoy.metrics import METRIC_PREFIX, METRICS

from .common import ENVOY_VERSION, HOST, INSTANCES, response

CHECK_NAME = 'envoy'


@pytest.mark.usefixtures('dd_environment')
def test_success(aggregator):
    instance = INSTANCES['main']
    c = Envoy(CHECK_NAME, {}, [instance])
    c.check(instance)

    metrics_collected = 0
    for metric in METRICS:
        metrics_collected += len(aggregator.metrics(METRIC_PREFIX + metric))

    assert metrics_collected >= 250


def test_success_fixture(aggregator):
    instance = INSTANCES['main']
    c = Envoy(CHECK_NAME, {}, [instance])

    with mock.patch('requests.get', return_value=response('multiple_services')):
        c.check(instance)

    metrics_collected = 0
    for metric in METRICS:
        metrics_collected += len(aggregator.metrics(METRIC_PREFIX + metric))

    num_metrics = len(response('multiple_services').content.decode().splitlines())
    num_metrics -= sum(c.unknown_metrics.values()) + sum(c.unknown_tags.values())
    assert 4412 <= metrics_collected == num_metrics


def test_success_fixture_whitelist(aggregator):
    instance = INSTANCES['whitelist']
    c = Envoy(CHECK_NAME, {}, [instance])

    with mock.patch('requests.get', return_value=response('multiple_services')):
        c.check(instance)

    for metric in aggregator.metric_names:
        assert metric.startswith('envoy.cluster.')


def test_success_fixture_blacklist(aggregator):
    instance = INSTANCES['blacklist']
    c = Envoy(CHECK_NAME, {}, [instance])

    with mock.patch('requests.get', return_value=response('multiple_services')):
        c.check(instance)

    for metric in aggregator.metric_names:
        assert not metric.startswith('envoy.cluster.')


def test_success_fixture_whitelist_blacklist(aggregator):
    instance = INSTANCES['whitelist_blacklist']
    c = Envoy(CHECK_NAME, {}, [instance])

    with mock.patch('requests.get', return_value=response('multiple_services')):
        c.check(instance)

    for metric in aggregator.metric_names:
        assert metric.startswith("envoy.cluster.") and not metric.startswith("envoy.cluster.out.")


def test_service_check(aggregator):
    instance = INSTANCES['main']
    c = Envoy(CHECK_NAME, {}, [instance])

    with mock.patch('requests.get', return_value=response('multiple_services')):
        c.check(instance)

    assert aggregator.service_checks(Envoy.SERVICE_CHECK_NAME)[0].status == Envoy.OK


def test_unknown():
    instance = INSTANCES['main']
    c = Envoy(CHECK_NAME, {}, [instance])

    with mock.patch('requests.get', return_value=response('unknown_metrics')):
        c.check(instance)

    assert sum(c.unknown_metrics.values()) == 5


@pytest.mark.parametrize(
    'test_case, extra_config, expected_http_kwargs',
    [
        ("new auth config", {'username': 'new_foo', 'password': 'new_bar'}, {'auth': ('new_foo', 'new_bar')}),
        ("legacy ssl config True", {'verify_ssl': True}, {'verify': True}),
        ("legacy ssl config False", {'verify_ssl': False}, {'verify': False}),
        ("legacy ssl config unset", {}, {'verify': True}),
    ],
)
def test_config(test_case, extra_config, expected_http_kwargs):
    instance = deepcopy(INSTANCES['main'])
    instance.update(extra_config)
    check = Envoy(CHECK_NAME, {}, instances=[instance])

    with mock.patch('datadog_checks.base.utils.http.requests') as r:
        r.get.return_value = mock.MagicMock(status_code=200)

        check.check(instance)

        http_wargs = dict(
            auth=mock.ANY, cert=mock.ANY, headers=mock.ANY, proxies=mock.ANY, timeout=mock.ANY, verify=mock.ANY
        )
        http_wargs.update(expected_http_kwargs)
        r.get.assert_called_with('http://{}:8001/stats'.format(HOST), **http_wargs)


def test_metadata(datadog_agent):
    instance = INSTANCES['main']
    check = Envoy(CHECK_NAME, {}, [instance])
    check.check_id = 'test:123'
    check.log = mock.MagicMock()

    with mock.patch('requests.get', side_effect=requests.exceptions.Timeout()):
        check._collect_metadata(instance['stats_url'])
        datadog_agent.assert_metadata_count(0)
        check.log.warning.assert_called_with(
            'Envoy endpoint `%s` timed out after %s seconds', 'http://localhost:8001/server_info', (10.0, 10.0)
        )
    with mock.patch('requests.get', side_effect=requests.exceptions.RequestException('Req Exception')):
        check._collect_metadata(instance['stats_url'])
        datadog_agent.assert_metadata_count(0)
        check.log.warning.assert_called_with(
            'Error collecting Envoy version with url=`%s`. Error: %s',
            'http://localhost:8001/server_info',
            'Req Exception',
        )

    with mock.patch('requests.get', return_value=response('multiple_services')):
        check._collect_metadata(instance['stats_url'])

        major, minor, patch = ENVOY_VERSION.split('.')
        version_metadata = {
            'version.scheme': 'semver',
            'version.major': major,
            'version.minor': minor,
            'version.patch': patch,
            'version.raw': ENVOY_VERSION,
        }

        datadog_agent.assert_metadata('test:123', version_metadata)
        datadog_agent.assert_metadata_count(len(version_metadata))


@pytest.mark.usefixtures('dd_environment')
def test_metadata_integration(aggregator, datadog_agent):
    instance = INSTANCES['main']
    c = Envoy(CHECK_NAME, {}, [instance])
    c.check_id = 'test:123'
    c.check(instance)

    major, minor, patch = ENVOY_VERSION.split('.')
    version_metadata = {
        'version.scheme': 'semver',
        'version.major': major,
        'version.minor': minor,
        'version.patch': patch,
        'version.raw': ENVOY_VERSION,
    }

    datadog_agent.assert_metadata('test:123', version_metadata)
    datadog_agent.assert_metadata_count(len(version_metadata))
