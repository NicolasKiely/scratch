import click
import dotenv

from definitions import ConfigException
dotenv.load_dotenv(".env")


@click.group()
def main():
    pass


def register_commands(root_group: click.Group):
    """ Register CLI commands """
    @root_group.group(name="trade")
    def trade_group():
        """ Trade commands """
        pass

    @root_group.group(name="coinbase")
    def coinbase_group():
        """ Coinbase API commands """
        pass

    @trade_group.command()
    def compute():
        """ Compute trades for portfolio """
        import trade_math
        import models

        asset_records = models.load_portfolio_data()
        trades = trade_math.compute_trades(asset_records)
        trade_df = models.save_computed_trades(trades)
        print(trade_df)

    @coinbase_group.command()
    def load_balance():
        """ Fetch account balance from coinbase """
        from coinbase_wrapper import CoinbaseAPI
        import models
        accounts = CoinbaseAPI.get_balances()
        balance_df = models.save_asset_balances(accounts)
        print(balance_df[balance_df["amount"] > 0])


if __name__ == "__main__":
    register_commands(main)
    try:
        main()
    except ConfigException as ex:
        print("Error: %s" % ex)
