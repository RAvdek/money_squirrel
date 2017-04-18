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
            KEYS['gpass']
        )
        self.start_dt = None
        self.end_dt = None
        self.request_payload = dict()
        self.data = []
        self.geo = None

    def _download_and_set_data(self):
        raise NotImplementedError

    def _correct_input(self):

        self.request_payload["timeframe"] = \
            " ".join([
                self.start_dt.strftime(utils.ISO_HOURLY),
                self.end_dt.strftime(utils.ISO_HOURLY)
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

    def load(
            self,
            kw_list,
            start_dt,
            end_dt,
            geo=None
    ):
        self.start_dt = start_dt
        self.end_dt = end_dt
        self.geo = geo
        self.request_payload = {
            "kw_list": kw_list,
            "geo": geo,
            "timeframe": None
        }
        self._correct_input()
        LOGGER.info(
            "Building payload for Trends API client:\n%s",
            self.request_payload
        )
        self.client.build_payload(**self.request_payload)
        LOGGER.info("Sending payload %s", self.request_payload)
        self._download_and_set_data()

    def store(self):
        for datum in self.data:
            record, created = self.MODEL.objects.get_or_create(**datum)
            if created:
                LOGGER.info("Storing data %s",
                            record)
                record.save()
            else:
                LOGGER.info("Record already exists: %s",
                            record)


class InterestOverTimeDownloader(TrendDownloader):

    MODEL = InterestOverTime

    def _download_and_set_data(self):
        new_data = self.client.interest_over_time()
        self._validate_new_data(new_data)
        new_data = new_data.T.to_dict()
        self.data = [
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

    def _download_and_set_data(self):
        new_data = self.client.interest_by_region()
        self._validate_new_data(new_data)
        new_data = new_data.T.to_dict()
        self.data = [
            {
                "start_dt": self.start_dt,
                "end_dt": self.end_dt,
                "geo": geo,
                "scores": new_data[geo],
            } for geo in self.data
        ]
