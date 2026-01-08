from internal.api_client import BackendClient
from helper.utils import Utils
from telebot import types
from telebot.async_telebot import AsyncTeleBot

class BotHandler:
    def __init__(self, api_client: BackendClient, utils: Utils) -> None:
        self.api_client = api_client
        self.utils = utils

    async def prompt(self, bot: AsyncTeleBot, message: types.Message):
        message_splitter = message.text.split(" ")
        parsed_elements = self.utils.parse_elements(message_splitter)
        parsed_filter = self.utils.strict_query_filter(parsed_elements)
        values_query = dict(parsed_elements.get("plain", ""))

        results = self.api_client.search(
            query=values_query.get("value"),
            filter=parsed_filter,
            limit=3
        )

        for result in results:
            sritct_values = self.utils.get_strict_values(elements=message_splitter)
            if self.utils.check_strict_values(strict_elements=sritct_values, result=result) or len(sritct_values) == 0:
                await bot.send_message(
                    message.chat.id,
                    str(result),
                    parse_mode="HTML"
                )
