"""Unit tests for Nebula agent."""

import json
import pathlib

from ostorlab.agent import definitions as agent_definitions
from ostorlab.runtimes import definitions as runtime_definitions
from ostorlab.utils import defintions as utils_definitions

from agent import nebula_agent
import pytest


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
