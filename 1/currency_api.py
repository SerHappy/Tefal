from datetime import datetime
from datetime import timedelta
from datetime import timezone
from decouple import config

import json
import requests


class JSONWriter:
    """Writes data to JSON file"""

    def __init__(self, filename: str) -> None:
        """
        Initialize JSONWriter class

        Args:
            filename (str): filename of JSON file
        """
        self.filename = filename

    def write_json(self, data: dict) -> None:
        """
        Writes data to JSON file

        Args:
            data (dict): data to write
        """
        with open(self.filename, "w") as file:
            json.dump(data, file, indent=2)


class CurrencyAPI:
    """Class for working with API"""

    def __init__(self) -> None:
        self._currency_url = config("URL", cast=str)
        self._currency_api = config("API_KEY", cast=str)

    def _send_request(self, params: dict) -> dict:
        """
        Sends a generic request to the API.

        Args:
            params (dict): Parameters for the request.

        Returns:
            dict: Raw JSON response.
        """
        request = requests.get(self._currency_url, params=params)
        return request.json()

    def _send_historical_request(self, date: str) -> dict:
        """
        Sends request to API for historical data.

        Args:
            date (str): date of data

        Returns:
            dict: Raw data
        """
        params = {
            "apikey": self._currency_api,
            "date": date,
            "base_currency": "RUB",
            "currencies": "USD,EUR",
        }
        return self._send_request(params)

    def _parse_data(self, data: dict, date: str) -> dict:
        """
        Returns parsed data.

        Args:
            data (dict): raw data
            date (str): date of data

        Returns:
            dict: parsed data
        """
        return data["data"].get(date, {})

    def _get_date_list(self) -> list:
        """
        Returns list of dates for last 7 days excluding today (current API limit).

        Returns:
            list: list of dates
        """
        today = datetime.now(timezone.utc).date()
        return [(today - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(7, 0, -1)]

    def get_statistic(self) -> dict:
        """
        Returns statistic for last 7 days excluding today.

        Returns:
            dict: JSON-formatted statistic for last 7 days
        """
        date_list = self._get_date_list()
        all_data = {}
        for date in date_list:
            raw_data = self._send_historical_request(date)
            parsed_data = self._parse_data(raw_data, date)
            all_data.update({date: parsed_data})

        result = {"data": all_data}
        return result


def main() -> None:
    """Main function"""
    api = CurrencyAPI()
    result = api.get_statistic()
    filename = f"statistic_{datetime.now(timezone.utc).strftime('%d-%m-%Y')}.json"
    writer = JSONWriter(filename=filename)
    writer.write_json(result)


if __name__ == "__main__":
    main()
