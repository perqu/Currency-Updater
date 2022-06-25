import requests
from decimal import Decimal


class RestNBP:
    def get_price(currency: str) -> Decimal:
        """
        Reads current value of provided currency\n
        Args:
            currency - currency symbol of type str
        Returns:
            price - current price of foreign currency of type Decimal
        """
        response = requests.get(
            f"http://api.nbp.pl/api/exchangerates/rates/C/{currency}/"
        )
        price = Decimal(response.json()["rates"][0]["ask"])
        return price
