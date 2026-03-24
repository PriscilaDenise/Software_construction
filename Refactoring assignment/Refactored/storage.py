import json
import os
import logging
from datetime import datetime
from config import DATA_FILE, DATE_FORMAT
from exceptions import DataStorageError

logger = logging.getLogger(__name__)


def current_time():
    return datetime.now().strftime(DATE_FORMAT)


def create_default_data():
    return {
        "clients": {
            "emma001": {
                "password": "1234",
                "full_name": "Emmanuel Nsubuga",
                "account_number": "100001",
                "balance": 500000.0,
                "transactions": [
                    {
                        "type": "Initial Deposit",
                        "amount": 500000.0,
                        "time": current_time()
                    }
                ]
            },
            "sarah001": {
                "password": "abcd",
                "full_name": "Sarah Namusoke",
                "account_number": "100002",
                "balance": 300000.0,
                "transactions": [
                    {
                        "type": "Initial Deposit",
                        "amount": 300000.0,
                        "time": current_time()
                    }
                ]
            }
        }
    }


def save_data(data):
    try:
        with open(DATA_FILE, "w") as file:
            json.dump(data, file, indent=4)
        logger.info("Data saved successfully.")
    except OSError as error:
        logger.error("Failed to save data: %s", error)
        raise DataStorageError("Could not save banking data.") from error


def load_data():
    try:
        if not os.path.exists(DATA_FILE):
            logger.warning("Data file not found. Creating default data.")
            data = create_default_data()
            save_data(data)
            return data

        with open(DATA_FILE, "r") as file:
            data = json.load(file)

        logger.info("Data loaded successfully.")
        return data

    except json.JSONDecodeError as error:
        logger.error("Invalid JSON format in data file: %s", error)
        raise DataStorageError("Bank data file is corrupted.") from error

    except OSError as error:
        logger.error("Failed to load data: %s", error)
        raise DataStorageError("Could not load banking data.") from error