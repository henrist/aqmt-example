#!/usr/bin/env python3
#
# This is an example of how to use the AQM test framework.
#
# Usage:
# ./example.py
#

import sys

from aqmt import Testbed, TestEnv, run_test, steps
from aqmt.plot import collection_components, flow_components
from aqmt.traffic import greedy


def test(result_folder):

    def my_test(testcase):
        testcase.traffic(greedy, node='a', tag='RENO')
        testcase.traffic(greedy, node='b', tag='CUBIC')

    testbed = Testbed()

    testbed.ta_samples = 50
    testbed.ta_delay = 250

    testbed.cc('a', 'reno', testbed.ECN_ALLOW)
    testbed.cc('b', 'cubic', testbed.ECN_ALLOW)

    run_test(
        folder=result_folder,
        title='Just a simple test to demonstrate simple usage',
        testenv=TestEnv(testbed),
        steps=(
            steps.plot_compare(level_order=[], components=[
                collection_components.utilization_tags(),
                collection_components.queueing_delay(),
                collection_components.drops_marks(),
            ]),
            steps.plot_flows(level_order=[], components=[
                flow_components.utilization_queues(),
                flow_components.rate_per_flow(),
                flow_components.rate_per_flow(y_logarithmic=True),
                flow_components.window(),
                flow_components.window(y_logarithmic=True),
                flow_components.queueing_delay(),
                flow_components.queueing_delay(y_logarithmic=True),
                flow_components.drops_marks(),
                flow_components.drops_marks(y_logarithmic=True),
            ]),
            steps.branch_sched([
                # tag, title, name, params
                ('pie', 'PIE', 'pie', 'ecn'),
                ('pfifo', 'pfifo', 'pfifo', ''),
                ('fq_codel', 'fq_codel', 'fq_codel', ''),
            ]),
            steps.branch_bitrate([
                10,
                50,
            ]),
            steps.branch_rtt([
                2,
                10,
                50,
            ], title='%d'),
            my_test,
        )
    )

if __name__ == '__main__':
    result_folder = 'results/example'
    if len(sys.argv) >= 2:
        result_folder = sys.argv[1]

    test(result_folder)
