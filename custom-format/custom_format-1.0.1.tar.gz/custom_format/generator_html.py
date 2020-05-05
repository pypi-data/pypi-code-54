from yattag import Doc
from yattag import indent


class OptionalHtml:
    def __init__(self):
        self._temp_features = {}
        self._temp_scenarios = {}

        self._sid = 0
        self._doc, self._tag, self._text, self._line = Doc(defaults={}).ttl()

        self._data = {
            "features": []
        }

        self.css_class = {
            "container": "container",
            "row": "row",
            "column": "column",
            "collapse": "collapsible",
            "collapse_content": "content",
            "table": "table",
            "table_row": "table-row",
            "table_header_checkbox": "cell tb-check color-bw",
            "table_header_describe": "cell tb-desc color-bw",
            "table_item": "cell"
        }

    # 組合表格header
    def _table_header(self):
        _css = self.css_class["table_row"]
        with self._tag('div', klass=_css):
            _css = self.css_class["table_header_checkbox"]
            with self._tag('div', klass=_css):
                self._doc.input(('onclick', 'checkAll(this)'), type='hidden', name="value")

            _css = self.css_class["table_header_describe"]
            with self._tag('div', klass=_css):
                self._line('label', 'Scenario')

    # 組合表格項目
    def _table_item(self, item):
        item_name = item["name"]
        item_tag = item["tag"]
        self._sid += 1

        _css = self.css_class["table_row"]
        with self._tag('div', klass=_css):
            e_id = f"{self._sid:05}"
            _css = self.css_class["table_item"]
            with self._tag('div', klass=_css):
                self._doc.input(type='checkbox', name="value", value=f"{item_tag}", id=e_id)

            with self._tag('div', klass=_css):
                self._line('label', f"{item_name}", ("for", f"{e_id}"))

    # 組合表格
    def _table(self, scenario_list):
        _css = self.css_class["table"]
        with self._tag('div', klass=_css):
            self._table_header()
            for item in scenario_list:
                self._table_item(item)

    # 合併卷軸與表格
    def _collapse_item(self, feature):
        _css = self.css_class["collapse"]
        feature_name = feature["name"]
        scenario_list = feature["scenarios"]

        with self._tag('label', klass=_css):
            self._text(f"{feature_name}")

        _css = self.css_class["collapse_content"]
        with self._tag('div', klass=_css):
            self._table(scenario_list)

    def _column(self, feature):
        _css = self.css_class["column"]
        with self._tag('div', klass=_css):
            self._collapse_item(feature)

    def _row(self, features):
        _css = self.css_class["row"]
        for i in range(0, len(features), 2):
            with self._tag('div', klass=_css):
                feature_1 = features[i]
                self._column(feature_1)

                if (i + 1) >= len(features):
                    continue

                feature_2 = features[i + 1]
                self._column(feature_2)

    def _container(self, feature):
        _css = self.css_class["container"]
        with self._tag('div', klass=_css):
            self._row(feature)

    def generator(self, data_list):
        self._container(data_list)
        # 加入換行
        html = indent(self._doc.getvalue())
        with open("optional.html", 'w', encoding="utf-8") as html_file:
            html_file.write(html)
