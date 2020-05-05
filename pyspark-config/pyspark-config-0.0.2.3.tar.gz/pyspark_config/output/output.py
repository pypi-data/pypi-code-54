from dataclasses import dataclass
from typing import List
from pyspark_config.transformations.transformation import Transformation
from pyspark_config.spark_utils.dataFrame_extended.dataframe_extended import DataFrame_Extended
from pyspark_config.yamlConfig.config import dataclass_json


@dataclass_json
@dataclass
class Output:
    type: str = None
    name: str = None
    path: str = None
    transformations: List[Transformation] = None

    def __apply_transformation__(self, df):
        """
        Apply multiple transformations to a dataFrame determined
        by the transformation configuration indicated in the `config`
        attribute of this class.

        :return: class:`DataFrame_Extended`. DataFrame as an output
        of the performed transformations.

        """
        if self.transformations:
            for trans in self.transformations:
                df = trans.transform(df=df)
        return df

    def save(self, df: DataFrame_Extended):
        pass
