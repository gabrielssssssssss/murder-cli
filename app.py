import os
import logging
import asyncio
from telebot import types
from telebot.async_telebot import AsyncTeleBot
from internal.handlers import BotHandler
from internal.api_client import BackendClient
from dotenv import load_dotenv
from helper.prettier import Prettier
from helper.utils import Utils

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger('TeleBot').setLevel(logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

class Application:
    def __init__(self) -> None:
        prettier = Prettier()
        utils = Utils()
        self.api_client = BackendClient(prettier=prettier, utils=utils)
        self.handler = BotHandler(api_client=self.api_client, utils=utils)
        self.bot = AsyncTeleBot(os.getenv("TELEGRAM_TOKEN"))

    def main(self) -> None:
        @self.bot.message_handler(func=lambda message: True)
        async def on_message(message: types.Message):
            await self.handler.search_query(bot=self.bot, message=message)

        @self.bot.callback_query_handler(func=lambda call: True)
        async def on_callback(call: types.CallbackQuery):
            if call.data.startswith("pagination_"):
                await self.handler.update_message(bot=self.bot, call=call)

        asyncio.run(self.bot.infinity_polling())

if __name__ == "__main__":
    app = Application()
    app.main()
