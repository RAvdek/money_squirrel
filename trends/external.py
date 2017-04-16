import dateutil
from pytrends.request import TrendReq
from money_squirrel import utils
from trends.models import InterestByRegion, InterestOverTime


KEYS = utils.load_config('keys')
LOGGER = utils.get_logger(__name__)


class TrendInterface(object):

    def __init__(self):
        self.client = TrendReq(
            KEYS['gmail'],
            KEYS['gpass']
        )
        self.kw_list = None
        self.start_date = None
        self.end_date = None
        self.geo_name = None
        self.start_hour = None
        self.end_hour = None
        self.time_frame = None
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
        self.time_frame = " ".join([self.start_time, self.end_time])

    def _store_interest_by_region(self):
        ibr_data = self.data['interest_by_region'].T.to_dict()
        for geo_name in ibr_data:
            ibr = InterestByRegion(
                geo_name=geo_name,
                start_time=dateutil.parser.parse(self.start_time),
                end_time=dateutil.parser.parse(self.end_time),
                scores=ibr_data[geo_name]
            )
            ibr.save()

    def _store_interest_over_time(self):
        iot_data = self.data['interest_over_time'].T.to_dict()
        for ts in iot_data:
            iot = InterestOverTime(
                geo_name=self.geo_name,
                timestamp=ts.to_datetime(),
                start_time=dateutil.parser.parse(self.start_time),
                end_time=dateutil.parser.parse(self.end_time),
                scores=iot_data[ts]
            )
            iot.save()

    def load(
            self,
            kw_list,
            start_date,
            end_date,
            geo_name=None,
            start_hour=None,
            end_hour=None
    ):
        self.kw_list = kw_list
        self.start_date = start_date
        self.end_date = end_date
        self.geo_name = geo_name
        self.start_hour = start_hour
        self.end_hour = end_hour
        self.time_frame = None
        self._correct_input()
        self.client.build_payload(
            kw_list=self.kw_list,
            geo=self.geo_name,
            timeframe=self.time_frame
        )
        self.data['interest_by_region'] = \
            self.client.interest_by_region()
        self.data['interest_over_time'] = \
            self.client.interest_over_time()

    def store(self):
        self._store_interest_by_region()
        self._store_interest_over_time()
