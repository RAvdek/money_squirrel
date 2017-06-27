import datetime as dt
from dateutil.parser import parse as dt_parse
from django.core.management.base import BaseCommand, CommandError
from gdax_api.external import QuoteDownloader
from bin import utils


class Command(BaseCommand):
    help = """
    Download historical price data from GDAX.
    Please use UTC timestamps :D
    """

    def add_arguments(self, parser):

        parser.add_argument(
            '--start_date',
            type=str,
            dest='start_date',
            nargs=1,
            help='Choose a start_date for download. Defaults 5 MINUTES prior to END_DATE'
        )
        parser.add_argument(
            '--end_date',
            type=str,
            dest='end_date',
            nargs=1,
            help='Choose a start_date for download. Defaults UTC now'
        )
        parser.add_argument(
            '--granularity',
            type=int,
            dest='granularity',
            nargs=1,
            help='Window in seconds for price history. Default 20'
        )
        parser.add_argument(
            '--max_failures',
            type=int,
            dest='max_failures',
            nargs=1,
            help='How many HTTP failures before shut down?'
        )
        parser.add_argument(
            '--product',
            type=str,
            dest='product',
            nargs='*',
            help='Products to download, eg. BTC-USD, LTC-BTC, etc. Multiple products possible.'
        )

    def handle(self, *args, **options):

        end_date = dt_parse(options['end_date'][0]) \
            if options['end_date'] \
            else dt.datetime.utcnow()
        start_date = dt_parse(options['start_date'][0]) \
            if options['start_date'] \
            else end_date - dt.timedelta(minutes=5)
        granularity = options['granularity'][0] if options['granularity'] else 60
        max_failures = options['max_failures'][0] if options['max_failures'] else 10
        product_list = options['product'] \
            if options['product'] \
            else utils.PRODUCT_LIST

        assert end_date > start_date

        qd = QuoteDownloader()
        qd.run(
            start_dt=start_date,
            end_dt=end_date,
            granularity=granularity,
            max_failures=max_failures,
            product_list=product_list
        )
