import logging
from mosportal.account import Account
from datetime import datetime

logger = logging.getLogger(__name__)


class WaterException(BaseException):
    pass


class Water(Account):
    def __init__(self, session, flat, paycode, **kwargs):
        super(Water, self).__init__(session, flat, paycode, **kwargs)
        self.__meter_list = []
        self.__last_update = None

    @property
    def meter_list(self):
        if self.__meter_list and self.skip_update:
            return self.__meter_list

        try:
            response = self.session.post(
                url="https://www.mos.ru/pgu/common/ajax/index.php",
                data={
                    "items[paycode]": str(self.paycode),
                    "ajaxModule": "Guis",
                    "ajaxAction": "getCountersInfo",
                    "items[flat]": str(self.flat),
                },
            )

            if 'error' in response and response['error']:
                raise WaterException(response['error'])

            self.__meter_list = [Meter.parse(item, self) for item in response['counter']]
            return self.__meter_list
        except BaseException as e:
            raise WaterException('Ошибка получения данных с моспортала %s' % e)

    async def skip_update(self):
        return self.__last_update and (datetime.now() - self.__last_update).total_seconds() < 30


class Meter:
    def __init__(self, **kwargs):
        self.counterId = kwargs['counterId']
        self.meter_id = kwargs['meter_id']
        self.water = kwargs['water']
        self.value = kwargs['value']
        self.checkup = kwargs.get('checkup', None)
        self.update_date = kwargs['update_date']
        self.friendly_name = kwargs.get('friendly_name', None)
        self.cur_val = kwargs.get('cur_val', None)
        self.period = datetime.now().strftime('%Y-%m-%d')
        self.consumption = kwargs.get('consumption', None)
        self.history_list = kwargs.get('history_list', [])

    @classmethod
    def parse(cls, rj, water):
        value, update_date, consumption, history_list = cls.__get_current_val(rj['indications'])
        return cls(
            counterId=rj['counterId'],
            meter_id=rj['num'][1:],
            value=value,
            update_date=update_date,
            checkup=datetime.strptime(rj['checkup'][:-6], '%Y-%m-%d'),
            consumption=consumption,
            history_list=history_list,
            water=water
        )

    @staticmethod
    def __get_current_val(indicator):
        value_list = []
        if type(indicator) is list:
            value_list = indicator
        else:
            value_list.append(indicator)

        consumption = None
        if len(value_list) > 1:
            value_list.sort(key=lambda x: float(x['indication']), reverse=True)
            consumption = round(float(value_list[0]['indication']) - float(value_list[1]['indication']), 2)

        obj = value_list[0]
        return float(obj['indication']), datetime.strptime(obj['period'][:-6], '%Y-%m-%d'), consumption, value_list

    async def upload_value(self):
        """
        Обновление значения счетчика в Моспортале
        :return:
        """
        logger.debug('пытаемся передать данные: счетчик=<%s>; значние=<%s>' % (self.meter_id, self.cur_val))
        rj = self.water.session.call_post(
            url="https://www.mos.ru/pgu/common/ajax/index.php",
            data={
                "ajaxAction": "addCounterInfo",
                "ajaxModule": "Guis",
                "items[flat]": str(self.water.flat),
                "items[indications][0][period]": self.period,
                "items[indications][0][counterNum]": str(self.counterId),
                "items[paycode]": str(self.water.paycode),
                "items[indications][0][num]": "",
                "items[indications][0][counterVal]": self.cur_val,
            }
        )

        if 'code' in rj and rj['code'] == 0:
            logger.debug('запрос успешно выполнен %s set value: %s' % (self.meter_id, self.cur_val))
            return True
        else:
            raise WaterException('%s'%rj.get('error', rj))
