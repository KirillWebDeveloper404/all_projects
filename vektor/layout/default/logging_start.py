import logging

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(module)s - %(funcName)s - %(lineno)d - %(message)s",
    level=logging.INFO,
    # handlers=[logging.FileHandler("bot.log"), logging.StreamHandler()],
)
