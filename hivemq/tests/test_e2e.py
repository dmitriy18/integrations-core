# (C) Datadog, Inc. 2020-present
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)
import pytest

from datadog_checks.dev.jmx import JVM_E2E_METRICS

pytestmark = [pytest.mark.e2e]

METRICS = [
    'hivemq.messages.dropped.count',
    'hivemq.messages.incoming.auth.count',
    'hivemq.messages.incoming.connect.count',
    'hivemq.messages.incoming.connect.mqtt3.count',
    'hivemq.messages.incoming.connect.mqtt5.count',
    'hivemq.messages.incoming.disconnect.count',
    'hivemq.messages.incoming.pingreq.count',
    'hivemq.messages.incoming.puback.count',
    'hivemq.messages.incoming.pubcomp.count',
    'hivemq.messages.incoming.publish.bytes.50th_percentile',
    'hivemq.messages.incoming.publish.bytes.75th_percentile',
    'hivemq.messages.incoming.publish.bytes.95th_percentile',
    'hivemq.messages.incoming.publish.bytes.98th_percentile',
    'hivemq.messages.incoming.publish.bytes.999th_percentile',
    'hivemq.messages.incoming.publish.bytes.99th_percentile',
    'hivemq.messages.incoming.publish.bytes.count',
    'hivemq.messages.incoming.publish.bytes.max',
    'hivemq.messages.incoming.publish.bytes.mean',
    'hivemq.messages.incoming.publish.bytes.min',
    'hivemq.messages.incoming.publish.bytes.snapshot_size',
    'hivemq.messages.incoming.publish.bytes.std_dev',
    'hivemq.messages.incoming.publish.count',
    'hivemq.messages.incoming.pubrec.count',
    'hivemq.messages.incoming.pubrel.count',
    'hivemq.messages.incoming.subscribe.count',
    'hivemq.messages.incoming.total.bytes.50th_percentile',
    'hivemq.messages.incoming.total.bytes.75th_percentile',
    'hivemq.messages.incoming.total.bytes.95th_percentile',
    'hivemq.messages.incoming.total.bytes.98th_percentile',
    'hivemq.messages.incoming.total.bytes.999th_percentile',
    'hivemq.messages.incoming.total.bytes.99th_percentile',
    'hivemq.messages.incoming.total.bytes.count',
    'hivemq.messages.incoming.total.bytes.max',
    'hivemq.messages.incoming.total.bytes.mean',
    'hivemq.messages.incoming.total.bytes.min',
    'hivemq.messages.incoming.total.bytes.snapshot_size',
    'hivemq.messages.incoming.total.bytes.std_dev',
    'hivemq.messages.incoming.total.count',
    'hivemq.messages.incoming.unsubscribe.count',
    'hivemq.messages.outgoing.auth.count',
    'hivemq.messages.outgoing.connack.count',
    'hivemq.messages.outgoing.disconnect.count',
    'hivemq.messages.outgoing.pingresp.count',
    'hivemq.messages.outgoing.puback.count',
    'hivemq.messages.outgoing.pubcomp.count',
    'hivemq.messages.outgoing.publish.bytes.50th_percentile',
    'hivemq.messages.outgoing.publish.bytes.75th_percentile',
    'hivemq.messages.outgoing.publish.bytes.95th_percentile',
    'hivemq.messages.outgoing.publish.bytes.98th_percentile',
    'hivemq.messages.outgoing.publish.bytes.999th_percentile',
    'hivemq.messages.outgoing.publish.bytes.99th_percentile',
    'hivemq.messages.outgoing.publish.bytes.count',
    'hivemq.messages.outgoing.publish.bytes.max',
    'hivemq.messages.outgoing.publish.bytes.mean',
    'hivemq.messages.outgoing.publish.bytes.min',
    'hivemq.messages.outgoing.publish.bytes.snapshot_size',
    'hivemq.messages.outgoing.publish.bytes.std_dev',
    'hivemq.messages.outgoing.publish.count',
    'hivemq.messages.outgoing.pubrec.count',
    'hivemq.messages.outgoing.pubrel.count',
    'hivemq.messages.outgoing.suback.count',
    'hivemq.messages.outgoing.total.bytes.50th_percentile',
    'hivemq.messages.outgoing.total.bytes.75th_percentile',
    'hivemq.messages.outgoing.total.bytes.95th_percentile',
    'hivemq.messages.outgoing.total.bytes.98th_percentile',
    'hivemq.messages.outgoing.total.bytes.999th_percentile',
    'hivemq.messages.outgoing.total.bytes.99th_percentile',
    'hivemq.messages.outgoing.total.bytes.count',
    'hivemq.messages.outgoing.total.bytes.max',
    'hivemq.messages.outgoing.total.bytes.mean',
    'hivemq.messages.outgoing.total.bytes.min',
    'hivemq.messages.outgoing.total.bytes.snapshot_size',
    'hivemq.messages.outgoing.total.bytes.std_dev',
    'hivemq.messages.outgoing.total.count',
    'hivemq.messages.outgoing.unsuback.count',
    'hivemq.messages.pending.total.count',
    'hivemq.messages.queued.count',
    'hivemq.messages.retained.current',
    'hivemq.messages.retained.mean.50th_percentile',
    'hivemq.messages.retained.mean.75th_percentile',
    'hivemq.messages.retained.mean.95th_percentile',
    'hivemq.messages.retained.mean.98th_percentile',
    'hivemq.messages.retained.mean.999th_percentile',
    'hivemq.messages.retained.mean.99th_percentile',
    'hivemq.messages.retained.mean.count',
    'hivemq.messages.retained.mean.max',
    'hivemq.messages.retained.mean.mean',
    'hivemq.messages.retained.mean.min',
    'hivemq.messages.retained.mean.snapshot_size',
    'hivemq.messages.retained.mean.std_dev',
    'hivemq.messages.retained.pending.total.count',
    'hivemq.messages.retained.queued.count',
    'hivemq.networking.bytes.read.current',
    'hivemq.networking.bytes.read.total',
    'hivemq.networking.bytes.write.current',
    'hivemq.networking.bytes.write.total',
    'hivemq.networking.connections.current',
    'hivemq.networking.connections.mean.50th_percentile',
    'hivemq.networking.connections.mean.75th_percentile',
    'hivemq.networking.connections.mean.95th_percentile',
    'hivemq.networking.connections.mean.98th_percentile',
    'hivemq.networking.connections.mean.999th_percentile',
    'hivemq.networking.connections.mean.99th_percentile',
    'hivemq.networking.connections.mean.count',
    'hivemq.networking.connections.mean.max',
    'hivemq.networking.connections.mean.mean',
    'hivemq.networking.connections.mean.min',
    'hivemq.networking.connections.mean.snapshot_size',
    'hivemq.networking.connections.mean.std_dev',
    'hivemq.persistence.executor.running.threads',
    'hivemq.persistence.executor.subscription.tasks',
    'hivemq.persistence.executor.total.tasks',
    'hivemq.sessions.overall.current',
    'hivemq.sessions.persistent.active',
    'hivemq.subscriptions.overall.current',
    'hivemq.system.os.global.memory.available',
    'hivemq.system.os.global.memory.swap.total',
    'hivemq.system.os.global.memory.swap.used',
    'hivemq.system.os.global.memory.total',
    'hivemq.system.os.global.uptime',
    'hivemq.system.os.process.memory.virtual',
    'hivemq.system.os.process.threads.count',
]
METRICS.extend(JVM_E2E_METRICS)


def test(dd_agent_check):
    aggregator = dd_agent_check(rate=True)

    for metric in METRICS:
        aggregator.assert_metric(metric)

    aggregator.assert_all_metrics_covered()
