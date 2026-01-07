from internal.api_client import BackendClient
from telebot import types
from telebot.async_telebot import AsyncTeleBot

class BotHandler:
    def __init__(self, api_client: BackendClient) -> None:
        self.api_client = api_client

    async def prompt(self, bot: AsyncTeleBot, message: types.Message):
        results = self.api_client.search(
            query="",
            filter="lastname='alain'",
            limit=10
        )

        for result in results:
            await bot.send_message(
                message.chat.id,
                str(result),
                parse_mode="HTML"
            )
