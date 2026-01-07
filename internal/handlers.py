from internal.api_client import BackendClient
from telebot import types
from telebot.async_telebot import AsyncTeleBot

class BotHandler():
    """
    Telegram bot handler for the murder-backend project.

    Manages incoming messages and events from the Telegram client.
    Acts as a bridge between the bot and the backend API.
    """

    def __init__(self, api_client: BackendClient) -> None:
        self.api_client = api_client

    async def prompt(self, application: AsyncTeleBot | None, message: types.Message):
        await application.send_message(message.chat.id, 'Founded!')