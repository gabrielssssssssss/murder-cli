"""
Basic Telegram client for the murder-backend project.

This client interacts with Telegram users based on a whitelist system,
allowing only authorized users to execute commands. All available commands 
and their usage instructions can be found in the project's README.md file.

Usage:
Import this module and initialize the Telegram client to start 
listening for messages from authorized users.
"""

import logging

from telegram import (
    Update    
)
from telegram.ext import (
    Application    
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

def main() -> None:
    """Run telegram bot & Init all application module"""

    application = Application.builder().token("TOKEN").build()
    
    # Run the bot until the user presses CTRL-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()