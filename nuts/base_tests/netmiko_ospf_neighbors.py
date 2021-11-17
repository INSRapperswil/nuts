"""Query OSPF neighbors of a device or count them."""
from typing import Callable, Dict, Any

import pytest
from nornir.core.filter import F
from nornir.core.task import MultiResult, Result
from nornir_netmiko import netmiko_send_command

from nuts.context import NornirNutsContext
from nuts.helpers.filters import filter_hosts
from nuts.helpers.result import AbstractHostResultExtractor, NutsResult


class OspfNeighborsExtractor(AbstractHostResultExtractor):
    def single_transform(self, single_result: MultiResult) -> Dict[str, Any]:
        neighbors = self._simple_extract(single_result)
        return {details["neighbor_id"]: details for details in neighbors}


class OspfNeighborsContext(NornirNutsContext):
    def nuts_task(self) -> Callable[..., Result]:
        return netmiko_send_command

    def nuts_arguments(self) -> Dict[str, Any]:
        return {"command_string": "show ip ospf neighbor", "use_textfsm": True}

    def nornir_filter(self) -> F:
        return filter_hosts(self.nuts_parameters["test_data"])

    def nuts_extractor(self) -> OspfNeighborsExtractor:
        return OspfNeighborsExtractor(self)


CONTEXT = OspfNeighborsContext


class TestNetmikoOspfNeighborsCount:
    @pytest.mark.nuts("neighbor_count")
    def test_neighbor_count(self, single_result: NutsResult, neighbor_count: Any) -> None:
        assert len(single_result.result) == neighbor_count


class TestNetmikoOspfNeighbors:
    @pytest.mark.nuts("neighbor_id")
    def test_neighbor_id(self, single_result: NutsResult, neighbor_id: Any) -> None:
        assert neighbor_id in single_result.result

    @pytest.mark.nuts("neighbor_id,neighbor_address")
    def test_neighbor_address(self, single_result: NutsResult, neighbor_id: Any, neighbor_address: Any) -> None:
        neighbor = single_result.result[neighbor_id]
        assert neighbor["address"] == neighbor_address

    @pytest.mark.nuts("local_port,neighbor_id")
    def test_local_port(self, single_result: NutsResult, local_port: Any, neighbor_id: Any) -> None:
        neighbor = single_result.result[neighbor_id]
        assert neighbor["interface"] == local_port

    @pytest.mark.nuts("neighbor_id,state")
    def test_state(self, single_result: NutsResult, neighbor_id: Any, state: Any) -> None:
        neighbor = single_result.result[neighbor_id]
        assert neighbor["state"] == state
