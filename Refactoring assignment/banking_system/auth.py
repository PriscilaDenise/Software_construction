import logging
from exceptions import AuthenticationError

logger = logging.getLogger(__name__)


def login(data):
    print("\n========== BANK LOGIN ==========")
    username = input("Enter username: ").strip()
    password = input("Enter password: ").strip()

    client = data["clients"].get(username)

    if not client or client["password"] != password:
        logger.warning("Failed login attempt for username: %s", username)
        raise AuthenticationError("Invalid username or password.")

    logger.info("User logged in successfully: %s", username)
    return username