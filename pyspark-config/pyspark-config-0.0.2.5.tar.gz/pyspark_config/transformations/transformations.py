from typing import List
from dataclasses import dataclass
import pyspark.sql.functions as F
from pyspark.sql.types import StringType

from pyspark_config.yamlConfig.config import dataclass_json


@dataclass_json
@dataclass
class Transformation:
    type: str = None

    def transform(self, df):
        pass

@dataclass_json
@dataclass
class Select(Transformation):
    type = "Select"
    cols: List[str] = None

    def transform(self, df):
        return df.select(self.cols)


@dataclass_json
@dataclass
class Filter(Transformation):
    type = "Filter"
    sql_condition: str = None

    def transform(self, df):
        return df.filter(self.sql_condition)


@dataclass_json
@dataclass
class FilterByList(Transformation):
    type = "FilterByList"
    col: str = None
    choice_list:List[str] = None

    def transform(self, df):
        return df.filter_by_list(
            col=self.col,
            choice_list=self.choice_list
        )


@dataclass_json
@dataclass
class Cast(Transformation):
    type = "Cast"
    col: str = None
    newCol: str = None
    fromType: str = None
    toType: str = None

    def transform(self, df):
        return df.cast(
            col=self.col,
            newCol=self.newCol,
            fromType=self.fromType,
            toType=self.toType)


@dataclass_json
@dataclass
class Normalization(Transformation):
    type = "Normalization"
    col: str = None
    newCol: str = None

    def transform(self, df):
        return df.normalization(
            col=self.col,
            newCol=self.newCol)


@dataclass_json
@dataclass
class SortBy(Transformation):
    type = "SortBy"
    column: str = None
    ascending: bool = False

    def transform(self, df):
        return df.sort(
            self.column,
            ascending=self.ascending)


@dataclass_json
@dataclass
class GroupBy(Transformation):
    type = "GroupBy"
    groupBy_col_list: List[str] = None
    sum_col_list: List[str] = None
    count_col_list:List[str]= None

    def transform(self, df):
        return df.groupby(
            groupBy_col_list=self.groupBy_col_list,
            sum_col_list=self.sum_col_list,
            count_col_list=self.count_col_list
        )


@dataclass_json
@dataclass
class Concatenate(Transformation):
    """
    Creates a column contatinating the indicated columns with a delimiter (Default: "").

    :param cols: List[String]
        Columns to concatenate. Column type must be a string
    :param name: String
        Column name of the concatenated column
    :param delimiter: String
        Specifies the boundary between separate columns in the concatenated sequence

    """
    type = "Concatenate"
    cols: List[str] = None
    name: str = None
    delimiter: str = ""

    def transform(self, df):
        func = lambda cols: self.delimiter.join([x if x is not None else "" for x in cols])
        concat_udf = F.udf(func, StringType())
        return df.withColumn(self.name, concat_udf(F.array(*self.cols)))


@dataclass_json
@dataclass
class Split(Transformation):
    type = "Split"
    column: str = None
    newCol: str = None
    delimiter: str = None

    def transform(self, df):
        return df.split(
            column=self.column,
            newCol=self.newCol,
            delimiter=self.delimiter)


@dataclass_json
@dataclass
class AddPerc(Transformation):
    type = "AddPerc"
    column: str = None
    perc_name: str = "perc"

    def transform(self, df):
        return df.add_perc(
            column=self.column,
            perc_name=self.perc_name)


@dataclass_json
@dataclass
class AddDate(Transformation):
    type = "AddDate"
    date: str = None

    def transform(self, df):
        return df.add_date(self.date)


@dataclass_json
@dataclass
class CollectList(Transformation):
    type = "CollectList"
    order_by: List[str] = None
    group_by_list: List[str] = None
    column_list: List[str] = None

    def transform(self, df):
        return df.collect_list(
            order_by=self.order_by,
            group_by_list=self.group_by_list,
            column_list=self.column_list
        )


@dataclass_json
@dataclass
class ListLength(Transformation):
    type = "ListLength"
    column: str = None

    def transform(self, df):
        return df.list_length(
            column=self.column
        )


@dataclass_json
@dataclass
class OneHotEncoder(Transformation):
    type = "OneHotEncoder"
    col: str = None
    newCol: str = None
    vocabSize: int = None

    def transform(self, df):
        return df.one_hot_encoder(
            col=self.col,
            newCol=self.newCol,
            vocabSize=self.vocabSize
        )


@dataclass_json
@dataclass
class ClusterDF(Transformation):
    type = "ClusterDF"
    cluster_col:str = None
    cluster_list:List[str] = None
    groupby_col_list: List[str]=None
    sum_col_list: List[str]=None
    count_col_list: List[str]=None

    def transform(self, df):
        return df.cluster_df(
            cluster_col=self.cluster_col,
            cluster_list=self.cluster_list,
            groupby_col_list=self.groupby_col_list,
            sum_col_list=self.sum_col_list,
            count_col_list=self.count_col_list
        )
