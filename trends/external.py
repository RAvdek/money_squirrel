import dateutil
import pandas as pd
from pytrends.request import TrendReq
from bin import utils
from models import InterestByRegion, InterestOverTime


KEYS = utils.load_config('keys')
LOGGER = utils.get_logger(__name__)


class TrendInterface(object):

    def __init__(self):
        self.client = TrendReq(
            KEYS['gmail'],
            KEYS['gpass']
        )
        self.start_date = None
        self.end_date = None
        self.start_hour = None
        self.end_hour = None
        self.request_payload = dict()
        self.data = {
            'interest_by_region': None,
            'interest_over_time': None
        }

    def _correct_input(self):
        if not self.start_hour:
            self.start_hour = 0
        self.start_hour = str(self.start_hour).zfill(2)
        if not self.end_hour:
            self.end_hour = 23
        self.end_hour = str(self.end_hour).zfill(2)
        self.start_time = self.start_date + "T" + self.start_hour
        self.end_time = self.end_date + "T" + self.end_hour
        self.request_payload["timeframe"] = \
            " ".join([self.start_time, self.end_time])

    def _store_interest_by_region(self):
        ibr_data = self.data['interest_by_region'].T.to_dict()
        for geo in ibr_data:
            ibr = InterestByRegion(
                geo=geo,
                start_time=dateutil.parser.parse(self.start_time),
                end_time=dateutil.parser.parse(self.end_time),
                scores=ibr_data[geo]
            )
            LOGGER.info("Storing interest by region %s", ibr)
            ibr.save()

    def _store_interest_over_time(self):
        iot_data = self.data['interest_over_time'].T.to_dict()
        for ts in iot_data:
            iot = InterestOverTime(
                geo=self.geo,
                timestamp=ts.to_datetime(),
                start_time=dateutil.parser.parse(self.start_time),
                end_time=dateutil.parser.parse(self.end_time),
                scores=iot_data[ts]
            )
            LOGGER.info("Storing interest over time %s", iot)
            iot.save()

    def _validate_data(self):
        try:
            assert type(self.data) is dict
            for key in self.data:
                assert type(self.data[key]) is pd.DataFrame
                assert self.data[key].shape != (0, 0)
        except AssertionError as e:
            LOGGER.critical(
                "Trends data invalid:\n%s",
                self.data
            )
            raise e

    def load(
            self,
            kw_list,
            start_date,
            end_date,
            geo=None,
            start_hour=None,
            end_hour=None
    ):
        self.start_date = start_date
        self.end_date = end_date
        self.start_hour = start_hour
        self.end_hour = end_hour
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
        LOGGER.info("Fetching interest by region")
        self.data['interest_by_region'] = \
            self.client.interest_by_region()
        LOGGER.info("Fetching interest over time")
        self.data['interest_over_time'] = \
            self.client.interest_over_time()
        LOGGER.info("Validating response")
        self._validate_data()

    def store(self):
        self._store_interest_by_region()
        self._store_interest_over_time()
