import requests
import re
import traceback
import time
import sys
from datetime import datetime
import pysnooper

from bs4 import BeautifulSoup
import pandas as pd


class StockDataScraper:
    #@pysnooper.snoop()
    def extract_stocktable_from_yahoo(self,
                                      stock_code,
                                      search_range=None,
                                      trim_unit='d'):
        dt_now = datetime.now()
        # 実質最大範囲
        default_searchrange = {
            'start_year': 1900,  # 開始年
            'start_month': 1,  # 月
            'start_day': 1,  # 日
            'end_year': dt_now.year,  # 終了年
            'end_month': dt_now.month,
            'end_day': dt_now.day
        }
        # 指定パラメータに応じた処理
        if isinstance(stock_code, str):
            try:
                stock_code = int(stock_code)
            except ValueError:
                traceback.print_exc()
                print('国内銘柄コードは数字を指定する！')
                return
        if trim_unit not in ['m', 'w', 'd']:
            raise KeyError('月足，日足，週足の指定は"m", "w", "d"のどれかを指定せよ！')
        if search_range is None:
            start_year = default_searchrange['start_year']
            start_month = default_searchrange['start_month']
            start_day = default_searchrange['start_day']
            end_year = default_searchrange['end_year']
            end_month = default_searchrange['end_month']
            end_day = default_searchrange['end_day']
        elif not isinstance(search_range, dict):
            raise TypeError('検索範囲は辞書型で指定')
        elif default_searchrange.keys() != search_range.keys():
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

        # データ収集
        endofdata_flag = False
        page_idx = 1
        colnames = None
        table_values = []
        n_retry_limit = 10
        retry_count = 0
        while not endofdata_flag:
            # 時系列データ掲載URL先にリクエスト
            url = f'https://info.finance.yahoo.co.jp/history/?code={stock_code}.T' \
                + f'&sy={start_year}&sm={start_month}&sd={start_day}' \
                + f'&ey={end_year}&em={end_month}&ed={end_day}&tm={trim_unit}&p={page_idx}'

            # リクエスト -> 200以外である場合は時間をおいてもう一度
            res = requests.get(url)
            if res.status_code != 200:
                if retry_count > n_retry_limit:
                    raise Exception(f'再試行回数上限{n_retry_limit}を越えたため終了')
                print(f'レスポンスが正常でなく，{res.status_code}を返すため再試行')
                sleep_time = 10 + retry_count * 10
                print(sleep_time, '秒後再試行')
                time.sleep(10 + retry_count * 10)
                retry_count += 1
                continue

            res = requests.get(url).text

            # Beautiful Soup で整形
            soup = BeautifulSoup(res, 'html.parser')

            # ソースコード内で，Tableがはじまるところを絞り込み
            stock_table = soup.find('div', class_='padT12 marB10 clearFix')
            if stock_table is None:
                raise AttributeError('引数に正しいパラメータが指定できていない．銘柄コードが不正？')

            # 進捗の抽出&表示
            proceeding = stock_table.find(
                'span', class_='stocksHistoryPageing yjS').text
            page_info = re.findall(r'\d+', proceeding)
            msg = f'\r{page_info[2]}ページ中{page_info[0]}ページ目を抽出中．' \
                + f'{int(page_info[1])/int(page_info[2])*100}%完了'
            sys.stdout.write(msg)
            sys.stdout.flush()

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