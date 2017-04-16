import datetime as dt
import GDAX
from bin import utils
from gdax.models import GDAXPrice

LOGGER = utils.get_logger(__name__)


class HistoricPriceInterface(GDAX.PublicClient):

    DATA_KEYS = [
        "timestamp",  # storing everything but this
        "low",
        "high",
        "open",
        "close",
        "volume"
    ]

    def __init__(self):
        super(GDAX.PublicClient, self).__init__()
        self.data = None
        self.product = None
        self.start_time = None
        self.end_time = None
        self.granularity = None

    def load(
            self,
            product,
            start_time,
            end_time,
            granularity
    ):
        """ Download historical prices """

        self.product = product
        self.start_time = start_time
        self.end_time = end_time
        self.granularity = granularity
        self.data = self.getProductHistoricRates(
            product=product,
            start=start_time,
            end=end_time,
            granularity=granularity
        )

    def store(self):

        for datum in self.data:
            gp = GDAXPrice()
            gp.dt = dt.datetime.fromtimestamp(datum[0])
            for i in range(1, len(self.DATA_KEYS)):
                setattr(
                    gp,
                    self.DATA_KEYS[i],
                    datum[i]
                )
            gp.save()
