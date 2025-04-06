from enum import Enum

import json
import logging
import requests
import time

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)


class Currencies(Enum):
    CNY = 'CNY'
    EUR = 'EUR'
    GBP = 'GBP'
    RUB = 'RUB'


class Converter:
    def __init__(self, amount, max_retries=3, retry_delay=2, timeout=10):
        self.amount = amount
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.timeout = timeout
        self.rates = self.get_rates()

    def get_rates(self):
        for attempt in range(self.max_retries):
            try:
                response = requests.get("https://api.exchangerate-api.com/v4/latest/USD", timeout=self.timeout)
                response.raise_for_status()
                data = response.json()
                rates = data['rates']
                return rates

            except requests.exceptions.RequestException as e:
                logger.error(f"Request failed (attempt {attempt + 1}/{self.max_retries}): {e}")
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay)
                else:
                    logger.error("Max retries reached. Unable to fetch rates.")
                    return None

            except (json.JSONDecodeError, KeyError) as e:
                logger.error(f"Error processing JSON response: {e}")
                return None

    def convert(self, currency):
        if currency in Currencies:
            return self.rates[currency] * self.amount
        raise ValueError(f'Invalid currency: {currency}')
