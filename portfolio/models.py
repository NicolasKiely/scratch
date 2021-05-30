import pandas

from definitions import AssetBalanceColumnName
from definitions import AssetBalances
from definitions import FileName
from definitions import PortfolioAssetRecord
from definitions import PortfolioAssetRecords
from definitions import PortfolioColumnName
from definitions import TradeRecords
from definitions import ComputedTradeColumnName


def load_portfolio_data(
        data_path: str = FileName.PORTFOLIO_CSV.value
) -> PortfolioAssetRecords:
    """ Loads portfolio data from local file

    :param data_path: Optional path to save data
    :return: List of portfolio asset records
    """
    portfolio_df: pandas.DataFrame = pandas.read_csv(data_path)

    portfolio_df[PortfolioColumnName.NORM_WEIGHT.value] = (
            portfolio_df[PortfolioColumnName.WEIGHT.value]
            / portfolio_df[PortfolioColumnName.WEIGHT.value].sum()
    )
    portfolio_df[PortfolioColumnName.NEW_BALANCE.value] = (
            portfolio_df[PortfolioColumnName.BALANCE.value].sum()
            * portfolio_df[PortfolioColumnName.NORM_WEIGHT.value]
    )

    asset_records: PortfolioAssetRecords = []
    for _, portfolio_row in portfolio_df.iterrows():
        record = PortfolioAssetRecord(
            asset_name=portfolio_row[PortfolioColumnName.ASSET_NAME.value],
            balance=portfolio_row[PortfolioColumnName.BALANCE.value],
            new_balance=portfolio_row[PortfolioColumnName.NEW_BALANCE.value]
        )
        asset_records.append(record)
    return asset_records


def save_computed_trades(
        trades: TradeRecords,
        data_path: str = FileName.COMPUTED_TRADES_CSV.value
) -> pandas.DataFrame:
    """ Saves list of trades

    @param trades: List of computed trades to save
    @param data_path: Optional path to save data
    @return: Saved dataframe
    """
    trade_df: pandas.DataFrame = pandas.DataFrame.from_records(
        [
            {
                ComputedTradeColumnName.FROM_ASSET.value: trade.from_asset_name,
                ComputedTradeColumnName.TO_ASSET.value: trade.to_asset_name,
                ComputedTradeColumnName.AMOUNT.value: trade.amount
            }
            for trade in trades
        ]
    )
    trade_df.to_csv(data_path, index=False)
    return trade_df


def save_asset_balances(
        balances: AssetBalances,
        data_path: str = FileName.ASSET_BALANCES_CSV.value
) -> pandas.DataFrame:
    """ Saves asset balances to data store """
    balance_df: pandas.DataFrame = pandas.DataFrame.from_records(
        [
            {
                AssetBalanceColumnName.ASSET_NAME.value: balance.asset_name,
                AssetBalanceColumnName.AMOUNT.value: balance.amount
            }
            for balance in balances
        ]
    )
    balance_df.to_csv(data_path, index=False)
    return balance_df
