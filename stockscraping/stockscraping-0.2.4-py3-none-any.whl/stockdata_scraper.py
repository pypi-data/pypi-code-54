import requests
import re
import traceback
import time
import sys
from datetime import datetime
# import pysnooper
import logging

from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm

logger = logging.getLogger()
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

# 株おじさんからスクレイピングする際のリクエスト上限回数
#sys.setrecursionlimit(20)


class StockDataScraper:
    def __init__(self):
        dt_now = datetime.now()
        # 実質最大範囲
        self.default_searchrange = {
            'start_year': 1900,  # 開始年
            'start_month': 1,  # 月
            'start_day': 1,  # 日
            'end_year': dt_now.year,  # 終了年
            'end_month': dt_now.month,
            'end_day': dt_now.day
        }

    def _retry(self):
        self.n_retry_limit = 20
        self.retry_count = 0
        if self.retry_count > self.n_retry_limit:
            raise Exception(f'再試行回数上限{self.n_retry_limit}を越えたため終了')
        sleep_time = 10 + self.retry_count * 10
        logger.info(sleep_time, '秒後再試行')
        time.sleep(10 + self.retry_count * 10)
        self.retry_count += 1

    def _validate_args(self, stock_code, search_range):
        dt_now = datetime.now()
        # 指定パラメータに応じた処理
        if isinstance(stock_code, str):
            try:
                stock_code = int(stock_code)
            except ValueError:
                traceback.print_exc()
                print('国内銘柄コードは数字を指定する！')
                return
        if search_range is None:
            start_year = self.default_searchrange['start_year']
            start_month = self.default_searchrange['start_month']
            start_day = self.default_searchrange['start_day']
            end_year = self.default_searchrange['end_year']
            end_month = self.default_searchrange['end_month']
            end_day = self.default_searchrange['end_day']
        elif not isinstance(search_range, dict):
            raise TypeError('検索範囲は辞書型で指定')
        elif self.default_searchrange.keys() != search_range.keys():
            raise KeyError('検索範囲指定に必要なパラメータがない')
        else:
            start_year = search_range['start_year']
            start_month = search_range['start_month']
            start_day = search_range['start_day']
            end_year = search_range['end_year']
            end_month = search_range['end_month']
            end_day = search_range['end_day']
            if dt_now < datetime(end_year, end_month, end_day):
                raise ValueError(
                    f'検索範囲終了時点を未来にできない．{dt_now.year}/{dt_now.month}/{dt_now.day}以前に指定せよ！'
                )
        return start_year, start_month, start_day, end_year, end_month, end_day

    def extract_stocktable_from_kabuoji3(self, stock_code, search_range=None):
        start_year, start_month, start_day, end_year, end_month, end_day = \
            self._validate_args(stock_code, search_range)

        # 1. 探索元ルートURLから探索する各年別のURLをスクレイピング
        logger.info(f'銘柄{stock_code}の日足データを指定範囲内すべて取得する．．')
        url = None
        stocks_each_year = None
        # 探索元として有効なURLを発掘
        logger.info('探索元として有効なURLを発掘')
        year_range = range(1983, 2021)
        for y in tqdm(sorted(year_range, reverse=True)):
            # 年代まで指定しないとなぜかソースが一部欠損するな
            url = f'https://kabuoji3.com/stock/{stock_code}/{y}/'
            headers = {
                "User-Agent":
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
                "Accept":
                "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            }
            res = requests.get(url, headers=headers)
            time.sleep(1)
            if res.status_code != 200:
                raise ValueError(
                    f'レスポンスが正常でなく，{res.status_code}を返す．鯖落ち？or指定の銘柄コードが存在しないか，DB自体ない？'
                )
            soup = BeautifulSoup(res.text, 'html.parser')
            stocks_each_year = soup.find('ul', class_='stock_yselect mt_10')
            if not stocks_each_year is None:
                break
        if stocks_each_year is None:
            logger.info('ソース元のテーブルデータが存在しない')
            return
        stocks_each_year = stocks_each_year.find_all('li')
        # 1インテックス目から年代別なのでそこから拾うようにした．だから[1:]としている
        stocks_each_year = [
            ey.find('a').get('href') for ey in stocks_each_year
        ][1:]
        # 必要な年代のみを選定
        from pathlib import Path
        try:
            stocks_each_year = [
                ey for ey in stocks_each_year
                if start_year <= int(Path(ey).name) <= end_year
            ]
        except ValueError:
            raise ValueError('絞り込み時に文字列型の年であるはずの値をintに変換できないイレギュラー')

        #2. テーブル取得
        # Header行
        # (Classから取らなかった理由は，ソースコードにゴミタグが含まれていて正確に取得できなかったため)
        if  stocks_each_year == []:
            logger.info('指定探索範囲に応じた年代絞り込みの結果，抽出が必要なかったため終了')
            return
        header_url = stocks_each_year[0]
        res = requests.get(header_url, headers=headers).text  # TODO:例外処理
        time.sleep(1)
        soup = BeautifulSoup(res, 'html.parser')
        table = soup.find_all('tr')
        th_cols = [col.text for col in table[0].find_all('th')]
        th_cols[-1] = '調整後終値'  # Yahoo Financeの表現と統一
        # Body行
        table_body = []
        start_date = datetime(start_year, start_month, start_day)
        end_date = datetime(end_year, end_month, end_day)
        for url in tqdm(sorted(stocks_each_year)):  # 年代の古い順から取り出す
            res = requests.get(url, headers=headers).text  # TODO:例外処理
            soup = BeautifulSoup(res, 'html.parser')
            table = soup.find_all('tr')
            for row in table[1:]:
                td_cols = [col.text for col in row.find_all('td')]
                row_date = td_cols[0]
                row_date = datetime.strptime(row_date, '%Y-%m-%d')
                # 探索行の日付が範囲指定開始日より前なら次の日へ，
                # 範囲指定終了日より後ならテーブル探索ループから抜ける
                if start_date > row_date:
                    continue
                if end_date < row_date:
                    break
                table_body.append(td_cols)
            time.sleep(1)

        # 3. 取得したデータをDataFrameに変換
        df_stock = pd.DataFrame(table_body, columns=th_cols)

        return df_stock

    #@pysnooper.snoop()
    def extract_stocktable_from_yahoo(self,
                                      stock_code,
                                      search_range=None,
                                      trim_unit='d'):
        start_year, start_month, start_day, end_year, end_month, end_day = \
            self._validate_args(stock_code, search_range)
        if trim_unit not in ['m', 'w', 'd']:
            raise KeyError('月足，日足，週足の指定は"m", "w", "d"のどれかを指定せよ！')

        # データ収集
        endofdata_flag = False
        page_idx = 1
        colnames = None
        table_values = []
        while not endofdata_flag:
            # 時系列データ掲載URL先にリクエスト
            url = f'https://info.finance.yahoo.co.jp/history/?code={stock_code}.T' \
                + f'&sy={start_year}&sm={start_month}&sd={start_day}' \
                + f'&ey={end_year}&em={end_month}&ed={end_day}&tm={trim_unit}&p={page_idx}'

            # リクエスト -> 200以外である場合は時間をおいてもう一度
            res = requests.get(url)
            if res.status_code != 200:
                logger.error(f'レスポンスが正常でなく，{res.status_code}を返すため再試行')
                self._retry()
                continue

            res = requests.get(url).text

            # Beautiful Soup で整形
            soup = BeautifulSoup(res, 'html.parser')

            # ソースコード内で，Tableがはじまるところを絞り込み
            stock_table = soup.find('div', class_='padT12 marB10 clearFix')
            if stock_table is None:
                errmsg = '引数に正しいパラメータが指定できていないか，ソース元のデータ欠落'+ \
                    'でテーブルデータが取れていない．銘柄コードが不正？'
                logger.error(errmsg)
                self._retry()
                continue

            # 進捗の抽出&表示
            proceeding = stock_table.find(
                'span', class_='stocksHistoryPageing yjS').text
            page_info = re.findall(r'\d+', proceeding)
            msg = f'\r{page_info[2]}ページ中{page_info[0]}ページ目を抽出中．' \
                + f'{int(page_info[1])/int(page_info[2])*100}%完了'
            logger.info(msg)

            # Tableの抽出
            stock_table = stock_table.find_all('tr')

            # Tableのヘッダを取得
            if page_idx != 1:
                colnames = [
                    col.text.replace('*', '')
                    for col in stock_table[0].find_all('th')
                ]

            # stock_tableが二行目から存在しない -> ページは終端まで到達しているので終了フラグを立て，continue
            if len(stock_table) == 1:
                endofdata_flag = True
                continue  # 終端の場合，以下処理されずWhileループを抜ける

            # Tableの各データを抽出 -> DataFrameに変換
            for table_row in stock_table[1:]:
                tds = table_row.find_all('td')
                values_row = []
                for table_col in tds:
                    data_text = table_col.text
                    # 日付カラムかそれ以外の数値かで，文字列処理の内容が異なる
                    if '年' in data_text:
                        data_text = re.split('[年月日]', data_text)
                        monthly_foot = data_text[2] == ''
                        if monthly_foot:
                            data_text = f'{data_text[0]}-{data_text[1].zfill(2)}'
                        else:
                            # 日足，週足なら「日」まで含める
                            data_text = f'{data_text[0]}-{data_text[1].zfill(2)}-{data_text[2].zfill(2)}'
                    else:
                        try:
                            data_text = data_text.replace(',', '')
                            data_text = int(data_text)
                        except ValueError:
                            # 株価データに数値以外の値が含まれているため整数型へ変換せずそのままpassする．
                            # e.g. https://info.finance.yahoo.co.jp/history/
                            #      ?code=2388.T&sy=1983&sm=1&sd=1&ey=2020&em=1&ed=31&tm=m&p=4
                            pass
                    values_row.append(data_text)
                table_values.append(values_row)

            # ページを1つ進める
            page_idx += 1

            # 規制回避
            time.sleep(1)

        # 収集したデータをDataFrameに変換
        df_result = pd.DataFrame(table_values, columns=colnames)
        df_result['日付'] = pd.to_datetime(df_result['日付'])
        return df_result