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
logger = logging.getLogger(__name__)

load_dotenv()

class Application:
    def __init__(self) -> None:
        prettier = Prettier()
        utils = Utils()
        self.api_client = BackendClient(prettier=prettier, utils=utils)
        self.handler = BotHandler(api_client=self.api_client)
        self.bot = AsyncTeleBot(os.getenv("TELEGRAM_TOKEN"))

    def main(self) -> None:

        @self.bot.message_handler(func=lambda message: True)
        async def on_message(message: types.Message):
            logger.info(f"New message from {message.chat.id}")
            await self.handler.prompt(bot=self.bot, message=message)

        asyncio.run(self.bot.infinity_polling())

if __name__ == "__main__":
    app = Application()
    app.main()
