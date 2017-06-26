import datetime as dt
from time import sleep
from requests.exceptions import ConnectionError
import pandas as pd
from pytrends.request import TrendReq
from bin import utils
from models import InterestByRegion, InterestOverTime


KEYS = utils.load_config('keys')
LOGGER = utils.get_logger(__name__)


class TrendDownloader(object):

    MODEL = None

    def __init__(self):
        self.client = TrendReq(
            KEYS['gmail'],
            KEYS['gpass'],
            tz=0
        )
        self.start_dt = None
        self.end_dt = None
        self.request_payload = dict()
        self.data = []
        self.geo = None

    def _download_and_clean(self):
        raise NotImplementedError

    @staticmethod
    def _build_timeframe(start_dt, end_dt):

        return " ".join([
            start_dt.strftime(utils.ISO_HOURLY),
            end_dt.strftime(utils.ISO_HOURLY)
        ])

    @staticmethod
    def _validate_new_data(new_data):
        try:
            assert type(new_data) is pd.DataFrame
        except AssertionError as e:
            LOGGER.critical(
                "Trends data invalid:\n%s",
                new_data
            )
            raise e

    def _store(self, data):
        for datum in data:
            record, created = self.MODEL.objects.get_or_create(**datum)
            if created:
                LOGGER.info("Storing data %s",
                            record)
                record.save()
            else:
                LOGGER.info("Record already exists: %s",
                            record)

    def run(
            self,
            kw_list,
            start_dt,
            end_dt,
            geo=None
    ):
        assert type(start_dt) is dt.datetime
        assert type(end_dt) is dt.datetime

        self.start_dt = start_dt
        self.end_dt = end_dt
        self.geo = geo
        request_payload = {
            "kw_list": kw_list,
            "geo": geo,
            "timeframe": self._build_timeframe(start_dt, end_dt)
        }
        LOGGER.info(
            "Building payload for Trends API client:\n%s",
            request_payload
        )
        self.client.build_payload(**request_payload)
        LOGGER.info("Sending payload to Trends API")
        new_data = self._download_and_clean()
        self._store(new_data)


class InterestOverTimeDownloader(TrendDownloader):

    MODEL = InterestOverTime

    def _download_and_clean(self):
        new_data = self.client.interest_over_time()
        self._validate_new_data(new_data)
        new_data = new_data.T.to_dict()
        return [
            {
                "start_dt": self.start_dt,
                "end_dt": self.end_dt,
                "geo": self.geo,
                "scores": new_data[ts],
                "dt": ts.to_pydatetime()
            } for ts in new_data
        ]


class InterestByRegionDownloader(TrendDownloader):

    MODEL = InterestByRegion

    def _download_and_clean(self):
        new_data = self.client.interest_by_region()
        self._validate_new_data(new_data)
        new_data = new_data.T.to_dict()
        return [
            {
                "start_dt": self.start_dt,
                "end_dt": self.end_dt,
                "geo": geo,
                "scores": new_data[geo],
            } for geo in self.data
        ]


class IOTHourlyFromConfigDownloader(InterestOverTimeDownloader):

    def __init__(self, config_name):
        super(IOTHourlyFromConfigDownloader, self).__init__()
        self.config = utils.load_config('interest_over_time')[config_name]

    def run(self, start_dt, end_dt, max_failures=10):

        # Go back in time starting with end date.
        # use weekly pulls to get hourly data
        # We should get 1 datapoint of overlap
        current_end_dt = end_dt
        current_start_dt = end_dt - dt.timedelta(days=7)
        failure_count = 0
        while current_end_dt > start_dt:
            try:
                # get all of the search terms
                super(IOTHourlyFromConfigDownloader, self).run(
                    self.config['kw_list'],
                    start_dt=current_start_dt,
                    end_dt=current_end_dt
                )
                # get each search term with tags
                for term in self.config['kw_list']:
                    kw_list = [' '.join([term, tag]) for tag in self.config['tags']]
                    super(IOTHourlyFromConfigDownloader, self).run(
                        kw_list,
                        start_dt=current_start_dt,
                        end_dt=current_end_dt
                    )
                current_end_dt = current_start_dt
                current_start_dt = current_end_dt - dt.timedelta(days=7)
            except ConnectionError:
                failure_count += 1
                LOGGER.warn(
                    "HTTP Connection failure. Failure count: {}"
                    .format(failure_count)
                )
                sleep(60)
                if failure_count >= max_failures:
                    raise RuntimeError(
                        "{} HTTP connection errors. Aborting."
                        .format(max_failures)
                    )


class IBRDailyFromConfigDownloader(InterestByRegionDownloader):

    def __init__(self, config_name):
        super(InterestByRegionDownloader, self).__init__()
        self.config = utils.load_config('interest_by_region')[config_name]

    def run(self, start_dt, end_dt, max_failures=0):

        # Go back in time starting with end date.
        # use weekly pulls to get hourly data
        # We should get 1 datapoint of overlap
        current_end_dt = end_dt
        current_start_dt = end_dt - dt.timedelta(days=1)
        failure_count = 0
        while current_end_dt > start_dt:
            try:
                # get all of the search terms
                super(InterestByRegionDownloader, self).run(
                    self.config['kw_list'],
                    start_dt=current_start_dt,
                    end_dt=current_end_dt
                )
                current_end_dt = current_start_dt
                current_start_dt = current_end_dt - dt.timedelta(days=1)
            except ConnectionError:
                failure_count += 1
                LOGGER.warn(
                    "HTTP Connection failure. Failure count: {}"
                    .format(failure_count)
                )
                sleep(60)
                if failure_count >= max_failures:
                    raise RuntimeError(
                        "{} HTTP connection errors. Aborting."
                        .format(max_failures)
                    )
