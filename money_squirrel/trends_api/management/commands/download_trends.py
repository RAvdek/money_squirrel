import datetime as dt
from dateutil.parser import parse as dt_parse
from django.core.management.base import BaseCommand, CommandError
from trends_api.external import IOTHourlyFromConfigDownloader


class Command(BaseCommand):
    help = """
    Download historical data from Google Trends with hour granularity
    WARNING: The API serves weird looking data. Doing the best I can with it!
    Please use UTC timestamps :D
    """

    def add_arguments(self, parser):

        parser.add_argument(
            '--start_date',
            type=str,
            dest='start_date',
            nargs=1,
            help='Choose a start_date for download. Defaults 1 WEEK prior to END_DATE'
        )
        parser.add_argument(
            '--end_date',
            type=str,
            dest='end_date',
            nargs=1,
            help='Choose a start_date for download. Defaults UTC now'
        )
        parser.add_argument(
            '--config',
            type=str,
            dest='config',
            default='coins',
            help='Choose a keyword config from config/interest_over_time.json'
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
            start_date = end_date - dt.timedelta(days=7)

        config = options['config']
        max_failures = options['max_failures']

        assert end_date > start_date

        downloader = IOTHourlyFromConfigDownloader(config)
        downloader.run(
            start_dt=start_date,
            end_dt=end_date,
            max_failures=max_failures
        )
