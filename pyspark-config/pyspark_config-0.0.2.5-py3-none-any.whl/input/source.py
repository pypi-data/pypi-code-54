from dataclasses import dataclass
from pyspark_config.yamlConfig.config import dataclass_json
from pyspark_config.spark_utils.dataframe_extended import DataFrame_Extended

@dataclass_json
@dataclass
class Source:
    type: str =None
    label: str =None
    path: str = None

    def apply(self, spark_session):
        pass


@dataclass_json
@dataclass
class Csv(Source):
    type="Csv"
    csv_path: str=None
    delimiter: str=';'

    def apply(self, spark_session):
        input=spark_session.read.option("delimiter", self.delimiter).csv(
           self.csv_path, header=True, mode="DROPMALFORMED"
        )
        input=DataFrame_Extended(
            df=input,
            spark_session=spark_session
        )
        return input


@dataclass
class Parquet(Source):
    type= "Parquet"
    parquet_path: str=None

    def apply(self, spark_session):
        input=spark_session.read.parquet(self.parquet_path)
        input=DataFrame_Extended(
            df=input,
            spark_session=spark_session
        )
        return input



