import pandas
from collections import namedtuple
from typing import List

asset_record = namedtuple("asset_record", ["asset", "balance", "new_balance"])
trade_record = namedtuple("trade_record", ["from_asset", "to_asset", "amount"])

portfolio_df = pandas.read_csv("data/portfolio.csv")

ASSET_COL = "asset"
BALANCE_COL = "balance"
WEIGHT_COL = "weight"
NORM_WEIGHT_COL = "weight_norm"
NEW_BALANCE_COL = "balance_new"

portfolio_df[NORM_WEIGHT_COL] = portfolio_df[WEIGHT_COL] / portfolio_df[WEIGHT_COL].sum()
portfolio_df[NEW_BALANCE_COL] = portfolio_df[BALANCE_COL].sum() * portfolio_df[NORM_WEIGHT_COL]

asset_records = []
for _, portfolio_row in portfolio_df.iterrows():
    record = asset_record(
        asset=portfolio_row[ASSET_COL],
        balance=portfolio_row[BALANCE_COL],
        new_balance=portfolio_row[NEW_BALANCE_COL]
    )
    asset_records.append(record)


def get_asset_delta(asset: asset_record):
    return asset.balance - asset.new_balance


def apply_trade(
        assets: List[asset_record], trade: trade_record
) -> List[asset_record]:
    new_assets = []
    for old_asset in assets:
        if old_asset.asset == trade.from_asset:
            new_balance = old_asset.balance - trade.amount
        elif old_asset.asset == trade.to_asset:
            new_balance = old_asset.balance + trade.amount
        else:
            new_balance = old_asset.balance

        new_asset = asset_record(
            asset=old_asset.asset,
            balance=new_balance,
            new_balance=old_asset.new_balance
        )
        new_assets.append(new_asset)
    return new_assets


def get_trade(assets: List[asset_record]) -> List[trade_record]:
    assets: List[asset_record] = sorted(
        assets, key=lambda a: get_asset_delta(a), reverse=True
    )
    egress_delta = get_asset_delta(assets[0])
    ingress_delta = get_asset_delta(assets[-1])

    trade_amt = min(egress_delta, -ingress_delta)
    total_balance = sum(a.balance for a in assets)
    if trade_amt < 0.001 * total_balance:
        return []

    trade = trade_record(
        from_asset=assets[0].asset,
        to_asset=assets[-1].asset,
        amount=trade_amt
    )
    adjused_assets = apply_trade(assets, trade)
    next_trades = get_trade(adjused_assets)

    return [trade] + next_trades


trades = get_trade(asset_records)
trade_df = pandas.DataFrame.from_records(
    [
        {
            "from_asset": trade.from_asset,
            "to_asset": trade.to_asset,
            "amount": trade.amount
        }
        for trade in trades
    ]
)
trade_df.to_csv("data/computed_trades.csv", index=False)
print(trade_df)
