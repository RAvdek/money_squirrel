import datetime as dt
from dateutil.parser import parse as dt_parse
from django.core.management.base import BaseCommand, CommandError
from gdax_api.external import QuoteDownloader


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
            default=20,
            help='Window in seconds for price history. Default 20'
        )
        parser.add_argument(
            '--max_failures',
            type=int,
            dest='max_failures',
            default=10,
            help='How many HTTP failures before shut down?'
        )

    def handle(self, *args, **options):

        if options['end_date']:
            end_date = dt_parse(options['end_date'])
        else:
            end_date = dt.datetime.utcnow()

        if options['start_date']:
            start_date = dt_parse(options['start_date'])
        else:
            start_date = end_date - dt.timedelta(minutes=5)

        granularity = options['granularity']
        max_failures = options['max_failures']

        assert end_date > start_date

        qd = QuoteDownloader()
        qd.run(
            start_dt=start_date,
            end_dt=end_date,
            granularity=granularity,
            max_failures=max_failures
        )