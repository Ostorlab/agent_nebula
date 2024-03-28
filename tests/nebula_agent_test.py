"""Unit tests for Nebula agent."""

import json
import os
import pathlib

import pytest
from ostorlab.agent import definitions as agent_definitions
from ostorlab.agent.message import message as msg
from ostorlab.runtimes import definitions as runtime_definitions
from ostorlab.utils import defintions as utils_definitions
from pyfakefs import fake_filesystem_unittest

from agent import nebula_agent


def testAgentNebula_whenUnsupportedFileType_raisesValueError() -> None:
    """Test that NebulaAgent raises ValueError when file type is not supported."""
    with pytest.raises(ValueError):
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
                        value=json.dumps("txt").encode(),
                    ),
                ],
                healthcheck_port=5301,
                redis_url="redis://guest:guest@localhost:6379",
            )
            nebula_agent.NebulaAgent(definition, settings)


def testAgentNebula_whenFileTypeIsJson_persistMessage(
        agent_definition: agent_definitions.AgentDefinition,
        agent_settings: runtime_definitions.AgentSettings,
        link_message: msg.Message,
) -> None:
    """Test that NebulaAgent persists message to json file."""
    os.environ["UNIVERSE"] = "43"
    with fake_filesystem_unittest.Patcher():
        expected_output = json.dumps(
            {"url": "https://ostorlab.co", "method": b"GET"},
            cls=nebula_agent.CustomEncoder,
        )
        nebula_test_agent = nebula_agent.NebulaAgent(agent_definition, agent_settings)

        nebula_test_agent.process(link_message)

        assert os.path.exists("/output/scan_43_messages")
        assert len(os.listdir("/output/scan_43_messages")) == 1
        with open("/output/scan_43_messages/v3.asset.link_messages.json") as file:
            assert sorted(json.load(file).items()) == sorted(
                json.loads(expected_output).items()
            )


def testAgentNebula_whenFileTypeIsJson_persistMultipleLinkMessages(
        agent_definition: agent_definitions.AgentDefinition,
        agent_settings: runtime_definitions.AgentSettings,
        multiple_link_messages: list[msg.Message],
) -> None:
    """Test that NebulaAgent persists multiple link messages to json file."""
    os.environ["UNIVERSE"] = "43"
    with fake_filesystem_unittest.Patcher():
        expected_output = [
            json.dumps(
                {"url": f"https://www.domain{i}.com", "method": b"GET"},
                cls=nebula_agent.CustomEncoder,
            )
            for i in range(0, 5)
        ]
        nebula_test_agent = nebula_agent.NebulaAgent(agent_definition, agent_settings)

        for message in multiple_link_messages:
            nebula_test_agent.process(message)

        file_path = "/output/scan_43_messages"
        assert os.path.exists(file_path)
        assert len(os.listdir(file_path)) == 1
        with open(f"{file_path}/v3.asset.link_messages.json", "r") as file:
            lines = file.readlines()
        assert len(lines) == len(expected_output)
        for line, expected_line in zip(lines, expected_output):
            assert line.strip() == expected_line.strip()


def testAgentNebula_whenFileTypeIsJson_persistMultipleMessages(
        agent_definition: agent_definitions.AgentDefinition,
        agent_settings: runtime_definitions.AgentSettings,
        multiple_messages: list[msg.Message],
) -> None:
    """Test that NebulaAgent persists multiple messages of different types to json files."""
    os.environ["UNIVERSE"] = "43"
    with fake_filesystem_unittest.Patcher():
        expected_output = [
            json.dumps(
                {"url": "https://www.domain.com", "method": b"GET"},
                cls=nebula_agent.CustomEncoder,
            ),
            json.dumps({"name": "www.domain.com"}, cls=nebula_agent.CustomEncoder),
            json.dumps(
                {"host": "192.168.1.1", "mask": "24"},
                cls=nebula_agent.CustomEncoder,
            ),
        ]
        nebula_test_agent = nebula_agent.NebulaAgent(agent_definition, agent_settings)

        for message in multiple_messages:
            nebula_test_agent.process(message)

        file_path = "/output/scan_43_messages"
        assert os.path.exists(file_path)
        assert len(os.listdir(file_path)) == 3
        assert os.path.exists(f"{file_path}/v3.asset.link_messages.json") is True
        with open(f"{file_path}/v3.asset.link_messages.json", "r") as file:
            lines = file.readlines()
        assert len(lines) == 1
        assert lines[0].strip() == expected_output[0].strip()
        assert os.path.exists(f"{file_path}/v3.asset.domain_name_messages.json") is True
        with open(f"{file_path}/v3.asset.domain_name_messages.json", "r") as file:
            lines = file.readlines()
        assert len(lines) == 1
        assert lines[0].strip() == expected_output[1].strip()
        assert os.path.exists(f"{file_path}/v3.asset.ip_messages.json") is True
        with open(f"{file_path}/v3.asset.ip_messages.json", "r") as file:
            lines = file.readlines()
        assert len(lines) == 1
        assert lines[0].strip() == expected_output[2].strip()
