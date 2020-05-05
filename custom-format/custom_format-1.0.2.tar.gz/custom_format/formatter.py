from behave.formatter.base import Formatter
from custom_format.generator_html import OptionalHtml
from behave.model import ScenarioOutline


# use command：behave -f custom_format.formatter:OptionFormatter -d -t "your_tags"
class OptionFormatter(Formatter):
    def __init__(self, stream_opener, config):
        super().__init__(stream_opener, config)
        self.stream = self.open()
        self._html = OptionalHtml()
        self.fid = None
        self.data_list = []
        self.feature_id = 0

    def feature(self, feature):
        feature_info = None
        scenario_list = []
        for scenario in feature.scenarios:
            if len(scenario.tags) > 0:
                scenario_tag = scenario.tags[0]
                if isinstance(scenario, ScenarioOutline):
                    scenario_tag = f"{scenario_tag.split('.<')[0]}.*"

                scenario_info = {
                    "tag": f"@{scenario_tag}",
                    "name": f"{scenario.name}"
                }
                scenario_list.append(scenario_info)

        if len(scenario_list) > 0:
            self.feature_id += 1
            feature_info = {
                "id": f"f{self.feature_id:04d}",
                "name": f"{feature.name}",
                "scenarios": scenario_list
            }

        if feature_info:
            self.data_list.append(feature_info)

    def close(self):
        self._html.generator(self.data_list)
        self.close_stream()

