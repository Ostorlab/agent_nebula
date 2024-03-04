"""Nebula agent: responsible for persisting all types of messages."""

import json
import logging
from datetime import datetime
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

CONFIG_HOME = "/root/.ostorlab"


class CustomEncoder(json.JSONEncoder):
    def default(self, obj: Any) -> Any:
        if isinstance(obj, bytes) is True:
            return obj.decode("utf-8")

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

    def process(self, message: m.Message) -> None:
        """Process the message and persist it to the file type and location specified in the agent definition.

        Args:
            message: The message to process.
        """
        logger.info("Processing message of selector : %s", message.selector)
        message_data: dict[str, Any] | None = message.data
        if message_data is None:
            logger.warning("Message data is empty")
            return None

        if self._file_type == "json":
            self._persist_to_json(message_data)

    def _persist_to_json(self, message_data: dict[str, Any]) -> None:
        """Persist the message data to a JSON file.

        Args:
            message_data: The message data to persist.
        """
        with open(
            f"{CONFIG_HOME}/messages_{datetime.now().strftime('%Y-%m-%d_%H-%M')}.json",
            "a",
        ) as file:
            file.write(json.dumps(message_data, cls=CustomEncoder) + "\n")

        logger.info("Message persisted")


if __name__ == "__main__":
    logger.info("starting agent ...")
    NebulaAgent.main()
