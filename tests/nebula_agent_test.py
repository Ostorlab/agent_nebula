"""Unit tests for Nebula agent."""

from ostorlab.agent.message import message as msg
from pytest_mock import plugin

from agent import nebula_agent


def testAgentNebula_whenFileTypeIsJson_shouldPersistMessageToJSONFile(
    nebula_test_agent: nebula_agent.NebulaAgent,
    link_message: msg.Message,
    mocker: plugin.MockerFixture,
) -> None:
    """Test Nebula Agent when file_type is json and single message,
    should persist message to JSON file."""
    open_mocker = mocker.patch("builtins.open", mocker.mock_open())

    nebula_test_agent.process(link_message)

    assert open_mocker.called is True
    path, _ = open_mocker.call_args[0]
    assert nebula_agent.CONFIG_HOME + "/messages_" in path
    assert any(
        "https://ostorlab.co" in call_arg
        for call_arg in open_mocker().write.call_args[0]
    )


def testAgentNebula_whenMultipleMessages_shouldAppendMessagesToJSONFile(
    nebula_test_agent: nebula_agent.NebulaAgent,
    multiple_link_messages: list[msg.Message],
    mocker: plugin.MockerFixture,
) -> None:
    """Test Nebula Agent when multiple messages, should append messages to JSON file."""
    open_mocker = mocker.patch("builtins.open", mocker.mock_open())

    for message in multiple_link_messages:
        nebula_test_agent.process(message)

    assert open_mocker.called is True
    assert open_mocker().write.call_count == len(multiple_link_messages)
    assert all(
        f"https://www.domain{i}.com" in call_arg
        for i, args_list in enumerate(open_mocker().write.call_args_list)
        for call_arg in args_list[0]
    )
