import os
from typing import Dict

from coinbase.wallet.client import Client

from definitions import AssetBalance
from definitions import AssetBalances
from definitions import ConfigException


class CoinbaseAPI:
    _client: Client = None

    @classmethod
    def get_client(cls) -> Client:
        """ Gets Coinbase client """
        if cls._client is None:
            try:
                key: str = os.environ["COINBASE_API_KEY"]
                secret: str = os.environ["COINBASE_API_SECRET"]
            except KeyError:
                raise ConfigException("COINBASE_API_KEY and COINTBASE_API_SECRET need to be set")
            cls._client = Client(key, secret)
        return cls._client

    @classmethod
    def get_balances(cls) -> AssetBalances:
        """ Gets account balances """
        client: Client = cls.get_client()
        account_holdings: Dict[str, float] = {}
        for account_record in client.get_accounts()["data"]:
            account_balance: Dict[str, str] = account_record.get("native_balance")
            if account_balance is None:
                continue
            balance_currency: str = account_record.get("currency")
            if balance_currency is None:
                continue

            if balance_currency not in account_holdings:
                account_holdings[balance_currency] = 0.0

            account_balance: float = float(
                account_balance.get("amount", "0.0")
            )
            account_holdings[balance_currency] += account_balance

        return [
            AssetBalance(asset_name=asset_name, amount=balance)
            for asset_name, balance in account_holdings.items()
        ]
