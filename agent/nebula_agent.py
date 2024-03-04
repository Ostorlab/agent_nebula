"""Nebula agent: responsible for persisting all types of messages."""

import logging

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


class NebulaAgent(agent.Agent):
    """Agent responsible for persisting all types of messages to file type specified in the agent definition."""

    def __init__(
        self,
        agent_definition: agent_definitions.AgentDefinition,
        agent_settings: runtime_definitions.AgentSettings,
    ) -> None:
        super().__init__(agent_definition, agent_settings)
        self._file_type = self.args.get("file_type")
        self._file_path = self.args.get("file_path")

    def process(self, message: m.Message) -> None:
        """Process the message and persist it to the file type and location specified in the agent definition.

        Args:
            message: The message to process.
        """
        logger.info("processing message of selector : %s", message.selector)
        # TODO (elyousfi5): add the logic to persist the message to the file type and location specified in the agent
        logger.info(
            "message persisted to file type: %s at location: %s",
            self._file_type,
            self._file_path,
        )


if __name__ == "__main__":
    logger.info("starting agent ...")
    NebulaAgent.main()
