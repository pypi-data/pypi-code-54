from opentelemetry.sdk.trace.export import Span
import json
import re

ASPECTO_BLOCK_VALUE = '__aspecto_field_blocked__'
BLOCK_FIELD_ACTION = 'block-field'
SCRAMBLE_FIELD_ACTION = 'scramble-field'
BLOCK_REQUEST_ACTION = 'block-request'


def scramble(value):
    if value is None or type(value) is bool:
        return value
    elif type(value) is int:
        return int(scramble(str(value)))
    elif type(value) is float:
        return float(scramble(str(value)))
    elif type(value) is list:
        for idx, x in enumerate(value):
            value[idx] = scramble(x)
        return value
    elif type(value) is dict:
        for key in value:
            value[key] = scramble(value[key])
        return value
    else:  # string..
        all1s = re.sub(r'\d', '1', value)
        return re.sub('[a-zA-Z]', 'x', all1s)


class PrivacyEngine:
    def __init__(
            self,
            privacy_rules: list
    ):
        self.privacy_rules = privacy_rules

    def execute_rules(self, span: Span):
        for rule in self.privacy_rules:
            block = self.execute_rule(rule, span)
            if block:
                return True
        return False

    def execute_rule(self, rule, span: Span):
        """Alters the span and returns if should block or not"""
        if self.conditions_met(rule["conditions"], span):
            should_block = self.execute_actions(rule["actions"], span)
            return should_block

    def execute_actions(self, actions: list, span: Span):
        for action in actions:
            action_type = action["actionType"]
            action_data = action["actionData"]  # {fieldTypes: str[], filter: { filterType: str, filterValue: str } }

            if action_type == SCRAMBLE_FIELD_ACTION or action_type == BLOCK_FIELD_ACTION:
                for field in action_data["fieldTypes"]:
                    filter_value = action_data["filter"]["filterValue"]

                    if field == "header":
                        self.apply_action_on_span_attribute(span, "http.request.headers", filter_value, action_type)
                        self.apply_action_on_span_attribute(span, "http.response.headers", filter_value, action_type)

                    elif field == "body-json":
                        self.apply_action_on_span_attribute(span, "http.request.body", filter_value, action_type)
                        self.apply_action_on_span_attribute(span, "http.response.body", filter_value, action_type)

                    elif field == "query-param":
                        self.apply_action_on_query_param(span, filter_value, action_type)

            elif action_type == BLOCK_REQUEST_ACTION:
                return True
            else:
                raise ValueError("Unsupported actionType of " + action_type)

        return False

    def apply_action_on_query_param(self, span: Span, filter_value: str, action_type: str):
        if "http.target" in span.attributes:
            url_key = "http.target"
        else:
            url_key = "http.url"

        split_target = span.attributes[url_key].split("?")
        if len(split_target) > 1:
            query_array = split_target[1].split("&")
            for idx, query in enumerate(query_array):
                queryKeyValuePair = query.split("=", 1)
                if queryKeyValuePair[0].lower() == filter_value.lower():
                    queryKeyValuePair[1] = ASPECTO_BLOCK_VALUE if action_type == BLOCK_FIELD_ACTION \
                        else scramble(queryKeyValuePair[1])
                    query_array[idx] = queryKeyValuePair[0] + "=" + queryKeyValuePair[1]
            span.attributes[url_key] = split_target[0] + "?" + "&".join(query_array)

    def apply_action_on_span_attribute(self, span: Span, attribute: str, filter_value: str, action_type: str):
        if attribute in span.attributes:
            span.attributes[attribute] = \
                self.apply_action_on_json_string(span.attributes[attribute], filter_value, action_type)

    def apply_action_on_json_string(self, json_string: str, json_key: str, action_type: str):
        if json_string == "" or json_string is None:
            return json_string
        try:
            as_json = json.loads(json_string)
            for key in as_json.keys():
                if json_key.lower() == key.lower():
                    if action_type == BLOCK_FIELD_ACTION:
                        as_json[key] = ASPECTO_BLOCK_VALUE

                    elif action_type == SCRAMBLE_FIELD_ACTION:
                        as_json[key] = scramble(as_json[key])

        except Exception:
            return json_string

        return json.dumps(as_json)

    def conditions_met(self, conditions: list, span: Span):
        for c in conditions:
            cType = c["conditionType"]
            if cType == "always":
                pass
            elif cType == "service":
                serviceName: str = span.attributes["aspecto.package.name"]
                if serviceName is None:
                    return False
                if not self.check_condition_filter(c["conditionData"], serviceName):
                    return False
            elif cType == "route":
                route: str = span.attributes["http.route"]
                if route is None:
                    return False
                """We check both flask route annotation (i.e. /users/<id>) and express style (i.e. /users/:id)"""
                if not self.check_condition_filter(c["conditionData"], route):
                    return False
                route = route.replace("<", ":").replace(">", "")
                if not self.check_condition_filter(c["conditionData"], route):
                    return False

        return True

    def check_condition_filter(self, filter_data: dict, value_to_check: str):
        filter_type = filter_data["filterType"]
        filter_value = filter_data["filterValue"]

        if filter_type == "by-value":
            return filter_value.lower() == value_to_check.lower()
        raise ValueError("Unsupported filterType of " + filter_type)
