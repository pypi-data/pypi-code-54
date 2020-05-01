import json
import pandas as pd
import numpy as np
import traceback
import base64
import re


class DataFrameDf(object):
    def __init__(self, df=None, *args, **kwargs):
        super(DataFrameDf, self).__init__(*args, **kwargs)
        self.df = df
        self.type_order = {'list': 2, 'dict': 1}

    def base64_decoder(self, names):
        """ 传入Dataframe
            所需要解码的列名"""
        for name in names:
            self.df[name] = self.df[name].apply(lambda x: base64.b64decode(x).decode('utf-8') if x is not None else x)
            self.df[name] = self.df[name].astype(np.str)

    def base64_encoder(self, names):
        """ 传入Dataframe
            所需要解码的列名"""
        for name in names:
            self.df[name] = self.df[name].astype(np.str)
            self.df[name] = self.df[name].apply(lambda x: base64.b64encode(x.encode('utf-8')).decode('utf-8')
                                                if x is not None else x)

    def drop(self, name):
        """namme: 丢掉的列"""
        try:
            self.df.drop(columns=name, inplace=True)
        except Exception as e:
            print(traceback.print_exc())

    def rename(self, rename_dict=None):
        """ 重命名列名"""
        if rename_dict is None:
            print("please enter rename dict")
        else:
            self.df.rename(columns=rename_dict, inplace=True)

    @staticmethod
    def _try_load(js):
        """
        尝试load数据, 错误的话返回空字典
        :param js:
        :return:
        """
        if isinstance(js, dict):
            return js
        try:
            js = json.loads(js)
        except:
            js = {}
        return js

    def _stracture_orgniser(self, srs):
        """
        整理传入的结构
        :param srs:
        :return:
        """
        stracture = set(srs)
        odict = dict()
        # 解析当前层结构，并且排序
        for stra in stracture:
            dct = json.loads(stra)
            for k, v in dct.items():
                if k not in odict:
                    odict[k] = self.type_order.get(v, 0)
                else:
                    if odict[k] != self.type_order.get(v, 0):
                        raise ValueError("json sctracture error! key=%s, diff values 【%s|%s】" % (k, odict[k], v))
        # 返回逆转的k, v值
        inv_map = dict()
        for k, v in odict.items():
            inv_map[v] = inv_map.get(v, [])
            inv_map[v].append(k)
        return inv_map

    def _json_df_parser(self, stra_type, cols, ex_col):
        """
        解析当前层次的数据，根据k进行抽取
        :param strc_type:
        :param cols:
        :param ex_col:
        :return:
        """
        if stra_type == 1:
            for k in cols:
                self.df[ex_col + '_' + k] = self.df[ex_col].apply(lambda x: x.get(k, {}))
        elif stra_type == 2:
            for k in cols:
                self.df[ex_col + '_' + k] = self.df[ex_col].apply(lambda x: x.get(k))
        else:
            for k in cols:
                self.df[ex_col + '_' + k] = self.df[ex_col].apply(lambda x: x.get(k))

    def _column_separator(self, col):
        """
        对于数据类型为列表的数据，进行行转列，然后拼接
        :param col:
        :return:
        """
        sep_df = self.df[col].copy().apply(lambda x: np.NaN if x == [] else x).replace("", np.NaN).dropna()
        # 判断下一层是否依然为字段，如果全是继续拆分，如果不是，终止
        all_dict = sep_df.apply(lambda x: np.array([isinstance(i, dict) for i in x]).all()).all()
        if all_dict:
            index_save = sep_df.index
            sep_df = sep_df.values.tolist()
            sep_df = pd.DataFrame(sep_df, index=index_save)
            sep_df = sep_df.stack()
            sep_df = sep_df.reset_index(level=-1, drop=True).to_frame().rename(columns={0: col})
            self.df.drop(columns=[col], inplace=True)
            self.df = self.df.join(sep_df, how='left')
            self.df.reset_index(inplace=True, drop=True)
            self._json_destroyer(ex_col=col)
        else:
            self.df[col] = self.df[col].astype(str)
            return False

    def _json_destroyer(self, ex_col=None):
        """
        利用递归对定规整类型的json组成的pandas列进行自动拆分和explode
        :param ex_col:
        :return:
        """
        # 试图加载json(传入必须为字典为起始步骤)
        self.df[ex_col] = self.df[ex_col].apply(lambda x: self._try_load(x))
        # 判断第一层的数据类型
        self.df['type_recorder'] = self.df[ex_col].apply(
            lambda x: json.dumps({k: str(type(v)).split("'")[1] for k, v in x.items()},
                                 ensure_ascii=False))
        stracture = self._stracture_orgniser(self.df['type_recorder'])
        print(stracture)
        # 遍历不同数据类型进行处理
        for key, value in stracture.items():
            self._json_df_parser(key, value, ex_col)
        # 因为ex_col是需要拆分的列，所以会删除
        self.df.drop(columns=[ex_col], inplace=True)
        # 对于数据类型为字典的情况
        for col in stracture.get(1, []):
            self._json_destroyer(ex_col=ex_col + '_' + col)

        # 对于数据类型为数组的情况
        for col in stracture.get(2, []):
            self._column_separator(ex_col + '_' + col)
        return stracture

    def json_sep_entance(self, ex_col, del_in_name=True):
        """
        制定单列报文进行拆分
        :param ex_col: 需要拆分的列名
        :param del_in_name: 是否删除入口名
        :return:
        """
        self._json_destroyer(ex_col)
        # 进行一些后处理工作
        self.df = self.df.fillna(np.NaN).replace("", np.NaN).drop(columns=['type_recorder']).drop_duplicates()
        # del_in_name = True的情况下，删除入口列名ex_col
        if del_in_name:
            self.df.columns = [re.sub(ex_col + '_', '', x) if x.startswith(ex_col) else x for x in list(self.df.columns)]

if __name__ == '__main__':
    df = pd.DataFrame({'aa': ['{"一年一班": [{"姓名": "张三"}, {"姓名": "李四"}],"一年二班":[{"姓名": "张三"}, {"姓名": "李四"}]}']})
    dfd = DataFrameDf(df)
    dfd.json_sep_entance(ex_col='aa')
    print(dfd.df)