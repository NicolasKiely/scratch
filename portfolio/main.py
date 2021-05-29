import click
import pandas


@click.group()
def main():
    pass


def register_commands(root_group: click.Group):
    """ Register CLI commands """
    @root_group.group(name="trade")
    def trade_group():
        """ Trade commands """
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


if __name__ == "__main__":
    register_commands(main)
    main()
