import datetime as dt
from time import sleep
import dateutil
import click
import utils
from gdax.external import HistoricPriceInterface
from trends.external import TrendInterface


LOGGER = utils.get_logger(__name__)
COINS = utils.load_config("coins")
ISO_DAILY = "%Y-%m-%d"
ISO_HOURLY = "%Y-%m-%dT%H"


class CoinDownloader(object):

    def __init__(
            self,
            start_date,
            end_date,
            coins=None,
            window_hours=6
    ):
        self.start_date = start_date
        self.end_date = end_date
        self.window_hours = window_hours
        if not coins:
            self.coins = list(COINS.keys())
        self.datetimes = [dateutil.parser.parse(start_date)]
        while self.datetimes[-1] <= dateutil.parser.parse(end_date):
            self.datetimes.append(self.datetimes[-1] + dt.timedelta(hours=window_hours))
        self.dates = [dateutil.parser.parse(start_date)]
        while self.dates[-1] <= dateutil.parser.parse(end_date):
            self.dates.append(self.dates[-1] + dt.timedelta(days=1))

    def _dl_gdax(self):
        gdax_client = HistoricPriceInterface()
        for coin in self.coins:
            for i, date in enumerate(self.dates):
                gdax_client.load(
                    product=coin.upper() + '-USD',
                    start_time=date.strftime(ISO_DAILY),
                    end_time=(date + dt.timedelta(days=1)).strftime(ISO_DAILY),
                    granularity=60*60*self.window_hours
                )
                gdax_client.store()
                # Public API limits to 3 / second
                # https://docs.gdax.com/#rate-limits
                sleep(1)

    def _dl_trends(self):
        trends_client = TrendInterface()
        for i, datetime in enumerate(self.datetimes):
            trends_client.load(
                kw_list=[COINS[c] for c in self.coins],
                start_date=datetime.strftime(ISO_DAILY),
                end_date=(datetime + dt.timedelta(hours=self.window_hours)).strftime(ISO_DAILY),
                start_hour=datetime.hour,
                end_hour=(datetime + dt.timedelta(hours=self.window_hours)).hour
            )

    def run(self):
        self._dl_gdax()
        self._dl_trends()


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

    dler = CoinDownloader(
        start_date=start_date,
        end_date=end_date,
        coins=coins,
        window_hours=window_hours
    )
    dler.run()

if __name__ == "__main__":

    main()
