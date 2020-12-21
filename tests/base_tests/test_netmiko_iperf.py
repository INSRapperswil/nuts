import pytest
from napalm.base.exceptions import ConnectionException
from nornir.core.task import AggregatedResult, MultiResult, Result

from pytest_nuts.base_tests.netmiko_iperf import transform_result
from tests.helpers.shared import create_result

test_data = [
    {"host": "L1", "destination": "10.0.0.2", "min_expected": 10000000},
    {"host": "L1", "destination": "10.0.0.3", "min_expected": 10000000},
    {"host": "L2", "destination": "10.0.0.1", "min_expected": 10000000},
]

result_data = [
    '{         "start": {            "connected": [                {                    "remote_host": "10.0.0.2"                }            ]        },        "end": {            "sum_received": {"bits_per_second": 3.298164e09}        }    }',
    '{        "start": {            "connected": [                {                    "remote_host": "10.0.0.3"                }            ]        },        "end": {            "sum_received": {"bits_per_second": 3.298164e09}        }    }',
    '{        "start": {            "connected": [                {                    "remote_host": "10.0.0.1"                }            ]        },        "end": {            "sum_received": {"bits_per_second": 0}        }    }',
    ]

@pytest.fixture
def general_result():
    ag_result = AggregatedResult("netmiko_iperf")

    overall_mr_l1 = MultiResult("netmiko_run_iperf")
    overall_mr_l1.append(Result(host=None, name="netmiko_run_iperf", result="iperf executed"))

    mr_l1_1 = MultiResult(name="_client_iperf")
    mr_l1_1.append(Result(host=None, name="_client_iperf", result="iperf executed"))
    l1_result1 = Result(host=None, name="netmiko_send_command")
    l1_result1.result = result_data[0]
    mr_l1_1.append(l1_result1)
    overall_mr_l1.append(mr_l1_1)

    mr_l1_2 = MultiResult(name="_client_iperf")
    mr_l1_2.append(Result(host=None, name="_client_iperf", result="iperf executed"))
    l1_result2 = Result(host=None, name="netmiko_send_command")
    l1_result2.result = result_data[1]
    mr_l1_2.append(l1_result2)
    overall_mr_l1.append(mr_l1_2)

    ag_result["L1"] = overall_mr_l1

    overall_mr_l2 = MultiResult("netmiko_run_iperf")
    overall_mr_l2.append(Result(host=None, name="netmiko_run_iperf", result="iperf executed"))
    mr_l2_1 = MultiResult(name="_client_iperf")
    mr_l2_1.append(Result(host=None, name="_client_iperf", result="iperf executed"))
    l2_result1 = Result(host=None, name="netmiko_send_command")
    l2_result1.result = result_data[2]
    mr_l2_1.append(l2_result1)
    overall_mr_l2.append(mr_l2_1)

    ag_result["L2"] = overall_mr_l2

    return ag_result

class TestTransformResult:
    @pytest.mark.parametrize("host", ["L1"])
    def test_contains_host_at_toplevel(self, general_result, host):
        transformed_result = transform_result(general_result)
        assert host in transformed_result

