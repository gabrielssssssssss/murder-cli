"""
Basic Telegram client for the murder-backend project.

This client interacts with Telegram users based on a whitelist system,
allowing only authorized users to execute commands. All available commands 
and their usage instructions can be found in the project's README.md file.

Usage:
Import this module and initialize the Telegram client to start 
listening for messages from authorized users.
"""

import os
import logging
import asyncio
from telebot import types
from telebot.async_telebot import AsyncTeleBot
from internal.handlers import BotHandler
from dotenv import load_dotenv

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

load_dotenv()

class Application(BotHandler):
    """
    Run telegram bot & Init all application module
    """
    def __init__(self) -> None:
        self.application = None

    def main(self) -> None:
        self.application = AsyncTeleBot(os.getenv("TELEGRAM_TOKEN"))

        @self.application.message_handler(func=lambda message:True)
        async def on_message(message: types.Message):
            logger.info(msg=f"New message from {message.chat.id}")
            await BotHandler.prompt(self, application=self.application, message=message)

        asyncio.run(self.application.infinity_polling())

if __name__ == "__main__":
    app = Application()
    app.main()
