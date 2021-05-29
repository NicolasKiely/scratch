""" Types and Constants """
from dataclasses import dataclass
from enum import Enum
from typing import List


@dataclass
class PortfolioAssetRecord:
    """ Represents an asset with a balance and a desired balance """
    asset_name: str
    balance: float
    new_balance: float


@dataclass
class TradeRecord:
    """ Represents trade from one asset to another """
    from_asset_name: str
    to_asset_name: str
    amount: float


# Plural of data classes
PortfolioAssetRecords = List[PortfolioAssetRecord]
TradeRecords = List[TradeRecord]


class PortfolioColumnName(Enum):
    """ Name of portfolio tabular data columns """
    ASSET_NAME = "asset"
    BALANCE = "balance"
    WEIGHT = "weight"
    NORM_WEIGHT = "weight_norm"
    NEW_BALANCE = "balance_new"


class ComputedTradeColumnName(Enum):
    """ Name of computed trade data columns  """
    FROM_ASSET = "from_asset"
    TO_ASSET = "to_asset"
    AMOUNT = "amount"


class FileName(Enum):
    """ Default name of data files """
    PORTFOLIO_CSV = "data/portfolio.csv"
    COMPUTED_TRADES_CSV = "data/computed_trades.csv"
