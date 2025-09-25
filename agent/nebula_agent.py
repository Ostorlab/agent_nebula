"""Nebula agent: responsible for persisting all types of messages."""

import base64
import json
import logging
import os
import pathlib
from typing import Any

from ostorlab.agent import agent, definitions as agent_definitions
from ostorlab.agent.message import message as m
from ostorlab.runtimes import definitions as runtime_definitions
from rich import logging as rich_logging

logging.basicConfig(
    format="%(message)s",
    datefmt="[%X]",
    level="INFO",
    force=True,
    handlers=[rich_logging.RichHandler(rich_tracebacks=True)],
)
logger = logging.getLogger(__name__)

SUPPORTED_FILE_TYPES = ["json"]


class CustomEncoder(json.JSONEncoder):
    def default(self, obj: Any) -> Any:
        if isinstance(obj, bytes) is True:
            return base64.b64encode(obj).decode("utf-8")
        return json.JSONEncoder.default(self, obj)


class NebulaAgent(agent.Agent):
    """Agent responsible for persisting all types of messages to file type specified in the agent definition."""

    def __init__(
        self,
        agent_definition: agent_definitions.AgentDefinition,
        agent_settings: runtime_definitions.AgentSettings,
    ) -> None:
        super().__init__(agent_definition, agent_settings)
        self._file_type = self.args.get("file_type", "json")
        if self._file_type.lower() not in SUPPORTED_FILE_TYPES:
            raise ValueError(
                f"File type {self._file_type} is not supported. Supported file types are {SUPPORTED_FILE_TYPES}"
            )
        self._output_directory: pathlib.Path
        output_directory: str | None = self.args.get("output_directory")
        if output_directory is not None:
            self._output_directory = pathlib.Path("/output") / os.path.basename(
                output_directory
            )
        else:
            self._output_directory = (
                pathlib.Path("/output") / f"scan_{self.universe}_messages"
            )
        self._output_directory.mkdir(parents=True, exist_ok=True)

    def process(self, message: m.Message) -> None:
        """Process the message and persist it to the file type and location specified in the agent definition.

        Args:
            message: The message to process.
        """
        logger.info("Processing message of selector : %s", message.selector)

        if self._file_type == "json":
            self._persist_to_json(message)

    def _persist_to_json(self, message_to_persist: m.Message) -> None:
        """Persist message to JSON file.

        Args:
            message_to_persist: The message to persist.
        """
        data = message_to_persist.data
        selector = message_to_persist.selector
        file_path = self._output_directory / f"{selector}_messages.json"

        with open(file_path, "a") as file:
            file.write(json.dumps(data, cls=CustomEncoder) + "\n")


if __name__ == "__main__":
    logger.info("starting agent ...")
    NebulaAgent.main()
