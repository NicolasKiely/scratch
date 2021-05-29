""" Math for computed trades to meet desired portfolio balance """
from definitions import PortfolioAssetRecord
from definitions import PortfolioAssetRecords
from definitions import TradeRecord
from definitions import TradeRecords


def get_asset_delta(asset: PortfolioAssetRecord) -> float:
    """ Gets the desired change in balance to meet the target balance """
    return asset.balance - asset.new_balance


def apply_trade(
        assets: PortfolioAssetRecords,
        trade: TradeRecord
) -> PortfolioAssetRecords:
    """ Recomputes assets as if a trade was a applied """
    new_assets: PortfolioAssetRecords = []
    for old_asset in assets:
        new_balance: float

        if old_asset.asset_name == trade.from_asset_name:
            new_balance = old_asset.balance - trade.amount
        elif old_asset.asset_name == trade.to_asset_name:
            new_balance = old_asset.balance + trade.amount
        else:
            new_balance = old_asset.balance

        new_asset = PortfolioAssetRecord(
            asset_name=old_asset.asset_name,
            balance=new_balance,
            new_balance=old_asset.new_balance
        )
        new_assets.append(new_asset)
    return new_assets


def compute_trades(assets: PortfolioAssetRecords) -> TradeRecords:
    """ Returns list of computed trades to reach desired balance """
    assets: PortfolioAssetRecords = sorted(
        assets, key=lambda a: get_asset_delta(a), reverse=True
    )
    egress_delta: float = get_asset_delta(assets[0])
    ingress_delta: float = get_asset_delta(assets[-1])

    trade_amt: float = min(egress_delta, -ingress_delta)
    total_balance: float = sum(a.balance for a in assets)
    if trade_amt < 0.001 * total_balance:
        return []

    trade: TradeRecord = TradeRecord(
        from_asset_name=assets[0].asset_name,
        to_asset_name=assets[-1].asset_name,
        amount=trade_amt
    )
    adjused_assets: PortfolioAssetRecords = apply_trade(assets, trade)
    next_trades: TradeRecords = compute_trades(adjused_assets)

    return [trade] + next_trades
