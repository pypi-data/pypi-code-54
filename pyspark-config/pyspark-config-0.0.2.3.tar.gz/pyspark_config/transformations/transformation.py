from dataclasses import dataclass

from pyspark_config.yamlConfig.config import dataclass_json


@dataclass_json
@dataclass
class Transformation:
    type: str = None

    def transform(self, df):
        pass
