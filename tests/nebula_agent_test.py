"""Unit tests for Nebula agent."""

import json
import os
import pathlib

import pytest
import ubjson
from ostorlab.agent import definitions as agent_definitions
from ostorlab.agent.message import message as msg
from ostorlab.runtimes import definitions as runtime_definitions
from ostorlab.utils import definitions as utils_definitions
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

        scan_dir = "/output/scan_43_messages"
        assert os.path.exists(scan_dir) is True
        assert len(os.listdir(scan_dir)) == 1
        message_dir = f"{scan_dir}/v3.asset.link_messages"
        assert os.path.exists(message_dir) is True
        assert len(os.listdir(message_dir)) == 1
        with open(f"{message_dir}/0.json") as file:
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

        scan_dir = "/output/scan_43_messages"
        assert os.path.exists(scan_dir) is True
        assert len(os.listdir(scan_dir)) == 1
        message_dir = f"{scan_dir}/v3.asset.link_messages"
        assert os.path.exists(message_dir) is True
        files = sorted(os.listdir(message_dir))
        assert len(files) == len(expected_output)
        for i, expected in enumerate(expected_output):
            with open(f"{message_dir}/{i}.json", "r") as f:
                content = f.read()
                assert content.strip() == expected.strip()


def testAgentNebula_whenFileTypeIsUbjson_persistMessage(
    agent_definition: agent_definitions.AgentDefinition,
    link_message: msg.Message,
) -> None:
    """Test that NebulaAgent persists message to ubjson file."""
    os.environ["UNIVERSE"] = "43"
    settings = runtime_definitions.AgentSettings(
        key="agent/ostorlab/nebula",
        bus_url="NA",
        bus_exchange_topic="NA",
        args=[
            utils_definitions.Arg(
                name="file_type",
                type="string",
                value=json.dumps("ubjson").encode(),
            ),
        ],
        healthcheck_port=5301,
        redis_url="redis://guest:guest@localhost:6379",
    )
    with fake_filesystem_unittest.Patcher():
        expected_output = {"url": "https://ostorlab.co", "method": b"GET"}
        nebula_test_agent = nebula_agent.NebulaAgent(agent_definition, settings)

        nebula_test_agent.process(link_message)

        scan_dir = "/output/scan_43_messages"
        assert os.path.exists(scan_dir) is True
        assert len(os.listdir(scan_dir)) == 1
        message_dir = f"{scan_dir}/v3.asset.link_messages"
        assert os.path.exists(message_dir) is True
        assert len(os.listdir(message_dir)) == 1
        with open(f"{message_dir}/0.ubjson", "rb") as file:
            assert ubjson.load(file) == expected_output


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

        scan_dir = "/output/scan_43_messages"
        assert os.path.exists(scan_dir) is True
        assert len(os.listdir(scan_dir)) == 3

        link_dir = f"{scan_dir}/v3.asset.link_messages"
        assert os.path.exists(link_dir) is True
        assert len(os.listdir(link_dir)) == 1
        with open(f"{link_dir}/0.json", "r") as file:
            assert file.read().strip() == expected_output[0].strip()

        domain_dir = f"{scan_dir}/v3.asset.domain_name_messages"
        assert os.path.exists(domain_dir) is True
        assert len(os.listdir(domain_dir)) == 1
        with open(f"{domain_dir}/0.json", "r") as file:
            assert file.read().strip() == expected_output[1].strip()

        ip_dir = f"{scan_dir}/v3.asset.ip_messages"
        assert os.path.exists(ip_dir) is True
        assert len(os.listdir(ip_dir)) == 1
        with open(f"{ip_dir}/0.json", "r") as file:
            assert file.read().strip() == expected_output[2].strip()


def testAgentNebula_whenMessagesDirnameIsSpecified_persistInMessagesDir(
    agent_definition: agent_definitions.AgentDefinition,
    agent_settings_with_messages_dir: runtime_definitions.AgentSettings,
    link_message: msg.Message,
) -> None:
    with fake_filesystem_unittest.Patcher():
        expected_output = json.dumps(
            {"url": "https://ostorlab.co", "method": b"GET"},
            cls=nebula_agent.CustomEncoder,
        )
        nebula_test_agent = nebula_agent.NebulaAgent(
            agent_definition, agent_settings_with_messages_dir
        )

        nebula_test_agent.process(link_message)

        output_dir = "/output/test_dir"
        assert os.path.exists(output_dir) is True
        assert len(os.listdir(output_dir)) == 1
        message_dir = f"{output_dir}/v3.asset.link_messages"
        assert os.path.exists(message_dir) is True
        assert len(os.listdir(message_dir)) == 1
        with open(f"{message_dir}/0.json") as file:
            assert sorted(json.load(file).items()) == sorted(
                json.loads(expected_output).items()
            )

def testAgentNebula_whenUtf8IsFalse_persistNormalJson(
    agent_definition: agent_definitions.AgentDefinition,
    link_message: msg.Message,
) -> None:
    os.environ["UNIVERSE"] = "43"
    settings = runtime_definitions.AgentSettings(
        key="agent/ostorlab/nebula",
        bus_url="NA",
        bus_exchange_topic="NA",
        args=[
            utils_definitions.Arg(
                name="utf8",
                type="boolean",
                value=json.dumps(False).encode(),
            ),
        ],
        healthcheck_port=5301,
        redis_url="redis://guest:guest@localhost:6379",
    )
    with fake_filesystem_unittest.Patcher():
        nebula_test_agent = nebula_agent.NebulaAgent(agent_definition, settings)
        nebula_test_agent.process(link_message)
        with open("/output/scan_43_messages/v3.asset.link_messages/0.json", "r") as file:
            content = file.read()
            assert "\n" not in content.strip()
            assert '"method": "R0VU"' in content

def testAgentNebula_whenUtf8IsTrue_persistBothJson(
    agent_definition: agent_definitions.AgentDefinition,
    link_message: msg.Message,
) -> None:
    os.environ["UNIVERSE"] = "43"
    settings = runtime_definitions.AgentSettings(
        key="agent/ostorlab/nebula",
        bus_url="NA",
        bus_exchange_topic="NA",
        args=[
            utils_definitions.Arg(
                name="utf8",
                type="boolean",
                value=json.dumps(True).encode(),
            ),
        ],
        healthcheck_port=5301,
        redis_url="redis://guest:guest@localhost:6379",
    )
    with fake_filesystem_unittest.Patcher():
        nebula_test_agent = nebula_agent.NebulaAgent(agent_definition, settings)
        nebula_test_agent.process(link_message)
        with open("/output/scan_43_messages/v3.asset.link_messages/0.json", "r") as file:
            lines = file.read().strip().split("\n")
            assert len(lines) == 2
            assert '"method": "R0VU"' in lines[0]
            assert '"method": "GET"' in lines[1]
