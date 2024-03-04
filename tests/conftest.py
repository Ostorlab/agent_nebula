"""Pytest fixtures for Agent Nebula."""

import json
import pathlib

import pytest
from ostorlab.agent import definitions as agent_definitions
from ostorlab.agent.message import message as msg
from ostorlab.runtimes import definitions as runtime_definitions
from ostorlab.utils import defintions as utils_definitions

from agent import nebula_agent


@pytest.fixture(scope="function", name="nebula_test_agent")
def fixture_agent(
    agent_mock: list[msg.Message],
    agent_persist_mock: dict[str | bytes, str | bytes],
) -> nebula_agent.NebulaAgent:
    """NebulaAgent fixture for testing purposes."""
    del agent_mock
    with (pathlib.Path(__file__).parent.parent / "ostorlab.yaml").open() as yaml_o:
        definition = agent_definitions.AgentDefinition.from_yaml(yaml_o)
        settings = runtime_definitions.AgentSettings(
            key="agent/ostorlab/nebula",
            bus_url="NA",
            bus_exchange_topic="NA",
            args=[
                utils_definitions.Arg(
                    name="file_type",
                    type="string",
                    value=json.dumps("json").encode(),
                ),
                utils_definitions.Arg(
                    name="file_path",
                    type="string",
                    value=json.dumps("output.json").encode(),
                ),
            ],
            healthcheck_port=5301,
            redis_url="redis://guest:guest@localhost:6379",
        )
        agent = nebula_agent.NebulaAgent(definition, settings)
        return agent


@pytest.fixture
def link_message() -> msg.Message:
    """Creates a dummy message of type v3.asset.link to be used by the agent for testing purposes."""
    selector = "v3.asset.link"
    msg_data = {"url": "https://ostorlab.co", "method": "GET"}
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
