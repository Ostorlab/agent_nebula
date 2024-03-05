"""Pytest fixtures for Agent Nebula."""

import pathlib

import pytest
from ostorlab.agent import definitions as agent_definitions
from ostorlab.agent.message import message as msg
from ostorlab.runtimes import definitions as runtime_definitions


@pytest.fixture(scope="function", name="agent_definition")
def agent_definition() -> agent_definitions.AgentDefinition:
    """NebulaAgent definition fixture for testing purposes."""
    with (pathlib.Path(__file__).parent.parent / "ostorlab.yaml").open() as yaml_o:
        return agent_definitions.AgentDefinition.from_yaml(yaml_o)


@pytest.fixture(scope="function", name="agent_settings")
def agent_settings() -> runtime_definitions.AgentSettings:
    """NebulaAgent settings fixture for testing purposes."""
    return runtime_definitions.AgentSettings(
        key="agent/ostorlab/nebula",
        bus_url="NA",
        bus_exchange_topic="NA",
        healthcheck_port=5301,
        redis_url="redis://guest:guest@localhost:6379",
    )


@pytest.fixture
def link_message() -> msg.Message:
    """Creates a dummy message of type v3.asset.link to be used by the agent for testing purposes."""
    selector = "v3.asset.link"
    msg_data = {"url": "https://ostorlab.co", "method": b"GET"}
    return msg.Message.from_data(selector, data=msg_data)


@pytest.fixture
def multiple_link_messages() -> list[msg.Message]:
    """Creates dummy messages of type v3.asset.link to be used by the agent for testing purposes."""
    selector = "v3.asset.link"
    return [
        msg.Message.from_data(
            selector, data={"url": f"https://www.domain{i}.com", "method": b"GET"}
        )
        for i in range(0, 5)
    ]


@pytest.fixture
def multiple_messages() -> list[msg.Message]:
    """Creates dummy messages of type v3.asset.link, v3.asset.domain, v3.asset.ip to be used by the agent for testing
    purposes."""
    return [
        msg.Message.from_data(
            "v3.asset.link", data={"url": "https://www.domain.com", "method": b"GET"}
        ),
        msg.Message.from_data("v3.asset.domain_name", data={"name": "www.domain.com"}),
        msg.Message.from_data(
            "v3.asset.ip", data={"host": "192.168.1.1", "mask": "24"}
        ),
    ]
