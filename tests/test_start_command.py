from src.lib import lib
from telegram.ext import ConversationHandler
import pytest
import asyncio
from pytest_mock import MockerFixture
from unittest.mock import AsyncMock  # Importa AsyncMock da unittest.mock

from src.start_command import start_command

@pytest.fixture
def update_mock(mocker: MockerFixture):
    return mocker.Mock()

@pytest.fixture
def context_mock(mocker: MockerFixture):
    return mocker.Mock()

@pytest.mark.asyncio
async def test_start_command(update_mock, context_mock, mocker):
    # Arrange
    update_mock.message = mocker.AsyncMock()
    update_mock.message.from_user = mocker.AsyncMock(first_name="John")
    spy = mocker.spy(start_command, "start_command")

    # Act
    result = await start_command(update_mock, context_mock)  # Aggiungi await qui

    # Assert
    assert result == ConversationHandler.END
    assert spy.call_count == 1
    await context_mock.bot.send_message.assert_called_once_with(
        chat_id=update_mock.effective_chat.id,
        text=f'Ciao John!\nBenvenuto nel bot di prenotazione del ristorante Da Tony&Ale.\nUsa:\n/prenota per effettuare una prenotazione\n/le_mie_prenotazioni per visualizzare le tue prenotazioni\n/menu per visualizzare il menu\n/eventi per gli eventi settimanali\n/info per le informazioni sul ristorante.'
    )
