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
        assert 24 % window_hours == 0

        self.start_date = start_date
        self.end_date = end_date
        self.window_hours = window_hours
        if not coins:
            self.coins = list(COINS.keys())
        # External interfaces
        self.gdax_client = HistoricPriceInterface()
        self.trends_client = TrendInterface()

    def _dl_gdax(self, date):
        date_string = date.strftime(ISO_DAILY)
        next_date = (date + dt.timedelta(days=1))
        next_date_string = next_date.strftime(ISO_DAILY)
        for coin in self.coins:
            self.gdax_client.load(
                product=coin.upper() + '-USD',
                start_time=date_string,
                end_time=next_date_string,
                granularity=60*60*self.window_hours
            )
            self.gdax_client.store()
            # Public API limits to 3 / second
            # https://docs.gdax.com/#rate-limits
            sleep(1)

    def _dl_trends(self, date):
        next_date = (date + dt.timedelta(days=1))
        datetime = date
        while datetime < next_date:
            next_datetime = (datetime + dt.timedelta(hours=self.window_hours))
            self.trends_client.load(
                kw_list=[COINS[c] + " currency"
                         for c in self.coins],
                start_date=datetime.strftime(ISO_DAILY),
                end_date=next_datetime.strftime(ISO_DAILY),
                start_hour=datetime.hour,
                end_hour=next_datetime.hour
            )
            self.trends_client.store()
            datetime = next_datetime

    def run(self):
        date_list = [dateutil.parser.parse(self.start_date)]
        while date_list[-1] <= dateutil.parser.parse(self.end_date):
            date_list.append(date_list[-1] + dt.timedelta(days=1))
        for date in date_list:
            LOGGER.info(
                "Downloading data for %s",
                date.strftime("ISO_DAILY"))
            self._dl_gdax(date)
            self._dl_trends(date)


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
