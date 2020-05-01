# -*- coding:utf-8 -*-
import re
import base64
import socket
from datetime import datetime
import datetime as dt
from dateutil.relativedelta import relativedelta
import requests


def get_host_ip(inner=True):
    """
    获取本机IP，inner=Tru是内网，False是外网
    :return:
    """
    if inner:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('8.8.8.8', 80))
            ip = s.getsockname()[0]
        finally:
            s.close()
    else:
        headers = {}
        headers['User-Agent'] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36"
        response = requests.get('http://ip.42.pl/raw', headers=headers)
        ip = response.text
    return ip


def calculate_age(born, end_date=datetime.today(), err_msg="error"):
    """
    计算年龄
    :param born: 传入出生日期 yyyyMMdd、yyyy-MM-dd、yyyy/MM/dd
    :param end_date: 默认为今天，也可以进行输入
    :return: 年龄
    """

    try:
        today = end_date
        if isinstance(end_date, str):
            today = re.sub('-|\/', '', today)
        elif isinstance(end_date, datetime):
            today = datetime.strptime(today, '%Y%m%d')
        else:
            raise TypeError("born: %s is not str or datetime" % type(end_date))

        if isinstance(born, str):
            born = re.sub('-|\/', '', born)
        elif isinstance(end_date, datetime):
            born = datetime.strptime(born, '%Y%m%d')
        else:
            raise TypeError("end_date: %s is not str or datetime" % type(end_date))
    except Exception as e:
        return err_msg

    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))


class DateCheck(object):
    def __init__(self, delimiter=''):
        if delimiter not in ['/', '-', '']:
            raise NotImplementedError("Date format not supported.\n"
                                      "Please enter one of the following format:"
                                      "1.yyyymmdd  2.yyyy-mm-dd 3.yyyy/mm/dd")
        self.normal_year = re.compile('(19[0-9]{2}|20[0-9]{2})%s((01|03|05|07|08|10|12)%s(0[1-9]|[1-2][0-9]|3[0-1])|'
                                      '(04|06|09|11)%s(0[1-9]|[1-2][0-9]|30)|02%s(0[1-9]|1[0-9]|2[0-8]))$'
                                      % tuple([delimiter] * 4))
        self.leap_year = re.compile('(19[0-9]{2}|20[0-9]{2})%s((01|03|05|07|08|10|12)%s(0[1-9]|[1-2][0-9]|3[0-1])|' 
                                    '(04|06|09|11)%s(0[1-9]|[1-2][0-9]|30)|02%s(0[1-9]|1[0-9]|2[0-9]))$'
                                    % tuple([delimiter] * 4))

    def check(self, date_str):
        """检查日期字符串是否合规"""
        if not isinstance(date_str, str):
            return None
        try:
            year = int(date_str[:4])
        except ValueError as e:
            return None
        if year % 4 == 0:
            pattern = self.leap_year
        else:
            pattern = self.normal_year
        if pattern.match(date_str):
            return date_str
        return None


class IdnExtractor(object):
    def __init__(self):
        self.idn_simple_pattern = re.compile('^\d{17}(\d|[xX])$')
        # 输入字符串
        self.istr = None

    def _check_valid(self, istr):
        """
        检查字符串是否大致符合身份证规则，否则返回空
        :param istr:
        :return:
        """
        try:
            self.istr = base64.b64decode(istr).decode('utf-8')
        except Exception as e:
            self.istr = istr
        if not isinstance(self.istr, str):
            return False
        if self.idn_simple_pattern.match(self.istr):
            return True
        else:
            return False

    def extract_age(self, istr, end_date=datetime.today()):
        """
        通过身份证计算年龄, 性别
        :param istr:
        :param end_date:
        :return:
        """
        if self._check_valid(istr):
            DC = DateCheck()
            birth_str = self.istr[6:14]
            birth_str = DC.check(birth_str)
            if birth_str is not None:
                age = calculate_age(birth_str, end_date)
            else:
                return None
        else:
            return None
        return age

    def extract_gender(self, istr):
        if self._check_valid(istr):
            gender = str(int(self.istr[16]) % 2)
            return gender
        else:
            return None


class PhoneCheck(object):
    "检查手机号是否合规"
    def __init__(self):
        # 电信
        self.pattern_dx = re.compile('^(86)?1((((33)|(49)|(53)|(8[019])|(7[37])|'
                                     '(99))\d{8})|(((349)|(410)|(70[0-2]))\d{7}))$')
        # 联通
        self.pattern_lt = re.compile('^(86)?1((((3[02])|(4[56])|(5[56])|(66)|(7[156])|'
                                     '(8[56]))\d{8})|((70[4789]\d{7})))$')
        # 移动
        self.pattern_yd = re.compile('^(86)?1((34[0-8]\d{7})|(((3[5-9])|(4[7-8])|(5[012789])|'
                                     '(7[28])|(8[23478])|(98))\d{8})|(((440)|(70[356]))\d{7}))$')

    def check(self, phone, operators=False):
        """
        查询手机号是否合规，如果合规返回手机号，不合规返回空。可选返回运营商
        :param phone:
        :param com: com=True,返回运营商
        :return:
        """
        if not isinstance(phone, str):
            return None
        if operators:
            if self.pattern_dx.match(phone):
                return '电信'
            elif self.pattern_lt.match(phone):
                return '联通'
            elif self.pattern_yd.match(phone):
                return '移动'
        else:
            if self.pattern_dx.match(phone):
                return phone
            elif self.pattern_lt.match(phone):
                return phone
            elif self.pattern_yd.match(phone):
                return phone
        return None


def create_assist_date(datestart=None, dateend=None,
                       infmt='%Y-%m-%d', ofmt='%Y-%m-%d',
                       unit='days', interval=1):
    """
    根据输入的开始结束时间，输出时间间隔列表
    :param datestart: 开始时间
    :param dateend: 结束时间
    :param infmt: 时间输入格式
    :param ofmt: 时间输出格式
    :param unit: 时间单位
    :param interval: 时间间隔
    :return:
    """

    # 转为日期格式
    datestart = datetime.strptime(datestart, infmt)
    o_datestart = datestart
    dateend = datetime.strptime(dateend, infmt)
    date_list = []
    # 判断方向
    if interval > 0:
        n = 1
        while o_datestart <= dateend:
            # 日期转字符串存入列表
            date_list.append(o_datestart.strftime(ofmt))
            o_datestart = _date_assistor(o_datestart, datestart, unit, interval, n)
            n += 1
    elif interval < 0:
        n = 1
        while o_datestart >= dateend:
            # 日期转字符串存入列表
            date_list.append(o_datestart.strftime(ofmt))
            o_datestart = _date_assistor(o_datestart, datestart, unit, interval, n)
            n += 1
    else:
        raise NotImplementedError("interval not correct")

    return date_list


def _date_assistor(datestart, unit, interval, n):
    # 日期叠加一天
    if unit == 'days':
        o_datestart = datestart + dt.timedelta(days=interval * n)
    elif unit == 'hours':
        o_datestart = datestart + dt.timedelta(hours=interval * n)
    elif unit == 'minutes':
        o_datestart = datestart + dt.timedelta(minutes=interval * n)
    elif unit == 'weeks':
        o_datestart = datestart + dt.timedelta(weeks=interval * n)
    elif unit == 'months':
        o_datestart = datestart + relativedelta(months=interval * n)
    elif unit == 'years':
        o_datestart = datestart + relativedelta(years=interval * n)
    else:
        raise NotImplementedError("%s is not an option for argument period!" % unit)
    return o_datestart


def strQ2B(ustring):
    """全角转半角"""
    rstring = ""
    for uchar in ustring:
        inside_code = ord(uchar)
        if inside_code == 12288:  # 全角空格直接转换
            inside_code = 32
        elif inside_code >= 65281 and inside_code <= 65374:  # 全角字符（除空格）根据关系转化
            inside_code -= 65248

        rstring += chr(inside_code)
    return rstring


def strB2Q(ustring):
    """半角转全角"""
    rstring = ""
    for uchar in ustring:
        inside_code = ord(uchar)
        if inside_code == 32:  # 半角空格直接转化
            inside_code = 12288
        elif inside_code >= 32 and inside_code <= 126:  # 半角字符（除空格）根据关系转化
            inside_code += 65248
        rstring += chr(inside_code)
    return rstring

if __name__ == '__main__':
    res = calculate_age("2019-06-01")
    print(res)
