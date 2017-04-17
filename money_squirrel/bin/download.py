import datetime as dt
from time import sleep
import dateutil
import click
import utils
from gdax.external import HistoricPriceInterface
from trends.external import TrendInterface


LOGGER = utils.get_logger(__name__)
COINS = utils.load_config("coins")


class CoinDownloader(object):

    def __init__(
            self,
            start_date,
            end_date,
            coins=None,
            window_hours=6,
            dl_trends=True,
            dl_gdax=True
    ):
        assert 24 % window_hours == 0

        self.start_dt = dateutil.parser.parse(start_date)
        self.end_dt = dateutil.parser.parse(end_date)
        self.window_hours = window_hours
        if not coins:
            self.coins = list(COINS.keys())
        self.dl_gdax = dl_gdax
        self.dl_trends = dl_trends
        # External interfaces
        self.gdax_client = HistoricPriceInterface()
        self.trends_client = TrendInterface()

    def _increment_dt(self, start_dt):
        return start_dt + dt.timedelta(hours=self.window_hours)

    def _dl_gdax(self, start_dt):
        # Have to iterate over the products
        for coin in self.coins:
            self.gdax_client.load(
                product=coin.upper() + '-USD',
                start_dt=start_dt,
                end_dt=self._increment_dt(start_dt),
                granularity=60*60
            )
            self.gdax_client.store()
            # Public API limits to 3 / second
            # https://docs.gdax.com/#rate-limits
            sleep(1)

    def _dl_trends(self, start_dt):
        self.trends_client.load(
            kw_list=[COINS[c] for c in self.coins],
            start_dt=start_dt,
            end_dt=self._increment_dt(start_dt)
        )
        self.trends_client.store()

    def run(self):
        query_dt = self.start_dt
        while query_dt < self.end_dt:
            LOGGER.info(
                "Downloading data for %s",
                query_dt.strftime(utils.ISO_HOURLY))
            if self.dl_gdax:
                self._dl_gdax(query_dt)
            if self.dl_trends:
                self._dl_trends(query_dt)
            query_dt = self._increment_dt(query_dt)


@click.option("--window_hours", "-w",
              help="How many hours is a time window?",
              default=6)
@click.option("--coins", "-c", multiple=True,
              help="Which coins to look up",
              default=list(COINS.keys()))
@click.argument("end_date")
@click.argument("start_date")
@click.command()
def main(start_date, end_date, window_hours, coins):

    downloader = CoinDownloader(
        start_date=start_date,
        end_date=end_date,
        coins=coins,
        window_hours=window_hours
    )
    downloader.run()

if __name__ == "__main__":

    main()
