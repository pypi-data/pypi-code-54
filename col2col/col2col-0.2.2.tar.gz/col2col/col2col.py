#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numbers
import logging
import pandas as pd
import json

logger = logging.getLogger('col2col')


def _condition(row, if_rule):
    value = None
    text = str()

    if isinstance(if_rule, dict):
        try:
            if if_rule['sense'] == '==':
                value = row[if_rule['key']] == if_rule['value']
                text = f" ( {if_rule['key']} == {if_rule['value']} ) "
            else:
                raise Exception("Unsupported if rule")
        except Exception:
            raise Exception("Malformed if rule")

    if isinstance(if_rule, list):
        # The first element is the operator
        operator = if_rule[0]
        if operator not in ['OR']:
            raise Exception("Unsupported if operator")

        # The second element is the list of operands
        otf_results = list()
        otf_text = list()
        for op in if_rule[1]:
            cond_result, cond_text = _condition(row, op)
            otf_results.append(cond_result)
            otf_text.append(cond_text)

        if operator == 'OR':
            value = any(otf_results)
            text = 'OR'.join(otf_text)

    return value, text


def _converter(x, ufrom, uto):

    if isinstance(x, numbers.Number):

        if ufrom == uto:
            y = x
        # POWER
        # from GWh/d to W
        elif ufrom == "GWh/d" and uto == "W":
            y = (x / 24) * 1e9
        # from W to GWh/d
        elif ufrom == "W" and uto == "GWh/d":
            y = (x / 1e9) * 24
        # LENGTH
        # from km to m   ////   from m to mm
        elif (ufrom == "km" and uto == "m") or (ufrom == "m" and uto == "mm"):
            y = x * 1000
        # from m to km   ////   from mm to m
        elif (ufrom == "m" and uto == "km") or (ufrom == "mm" and uto == "m"):
            y = x / 1000
        # from inches to m
        elif ufrom == "inches" and uto == "m":
            y = (x / 2.54) / 100
        # from m to inches
        elif ufrom == "m" and uto == "inches":
            y = x * 39.3701
        # PRESSURE
        # from bar to Pa
        elif ufrom == "bar" and uto == "Pa":
            y = x * 100000
        # from Pa to bar
        elif ufrom == "Pa" and uto == "bar":
            y = x / 100000
        # TEMPERATURE
        # from celsius to K
        elif ufrom == "celsius" and uto == "K":
            y = x + 273.15
        # from K to celsius
        elif ufrom == "K" and uto == "celsius":
            y = x - 273.15

        else:
            raise Exception("Unknown rule: from {fr} to {to}".format(fr=ufrom, to=uto))
    else:
        y = x

    return y


def col2col(df_collection, map_rules, reverse: bool = False):

    # Processing each data-frame (~sheet)
    for df_key, df in df_collection.items():

        if df_key not in map_rules.keys():
            # No rules, no work
            continue

        logger.debug(f" Sheet {df_key}")

        # Setup column names (via header key)
        header_index = map_rules[df_key]['header']
        if header_index < 1:
            # No header (it's possible?) means 'I can't identify columns'
            continue
        df.columns = df.iloc[header_index-1]

        # Get sheet rules
        rules = map_rules[df_key]['rules']

        # Processing each column
        for dfc in df.columns:

            if dfc not in rules.keys():
                # No rules, no work
                continue

            # Get a list of rules to apply to this column
            if isinstance(rules[dfc], list):
                rules_to_apply = rules[dfc]
            else:
                rules_to_apply = [rules[dfc]]

            # Check rules
            if len(rules_to_apply) > 1 and any(['if' not in r.keys() for r in rules_to_apply]):
                raise Exception("Trying to apply 'not conditional' rules to the same key")

            # Apply the rules
            for rule in rules_to_apply:

                if not isinstance(rule, dict):
                    # A rule must be a dictionary
                    raise Exception("Wrong rule syntax")

                # Get from-to pair units
                if reverse is False:
                    ufrom = rule['from']
                    uto = rule['to']
                else:
                    ufrom = rule['to']
                    uto = rule['from']

                if 'if' in rule.keys():
                    # Conditional rule => iterating over rows
                    for index, row in df.iterrows():
                        row_meets_condition, text_condition = _condition(row, rule['if'])
                        if row_meets_condition:
                            old_value = row[dfc]
                            row[dfc] = _converter(row[dfc], ufrom, uto)
                            logger.debug(f"  - @{dfc} ({text_condition}):  {old_value} -> {row[dfc]}")
                else:
                    # Simple rule
                    df[dfc] = df[dfc].apply(_converter, args=(ufrom, uto))
                    logger.debug(f"  - @{dfc}: {ufrom} -> {uto}")

    return


def col2col_fromfile(in_xlsx, out_xlsx, map_json, reverse: bool = False):
    # Load map (rules)
    with open(map_json, 'r') as f:
        map_rules = json.load(f)

    # Load input
    with pd.ExcelFile(in_xlsx) as xls:
        df_collection = {sheet: pd.read_excel(xls, sheet, header=None, index_col=None, na_values=['NA'])
                         for sheet in xls.sheet_names}

    col2col(df_collection, map_rules, reverse=reverse)

    # Saving resulting data-frame
    with pd.ExcelWriter(out_xlsx) as writer:
        for df_key, df in df_collection.items():
            df.to_excel(writer, sheet_name=df_key, index=None, header=None)
