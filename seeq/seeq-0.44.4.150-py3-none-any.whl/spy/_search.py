import re

import pandas as pd
import numpy as np

from seeq.sdk import *

from . import _common
from . import _config
from . import _login
from . import _push

from ._common import Status

from seeq import spy


def search(query, *, all_properties=False, workbook=_common.DEFAULT_WORKBOOK_PATH, recursive=True,
           include_archived=False, quiet=False, status=None):
    """
    Issues a query to the Seeq Server to retrieve metadata for signals,
    conditions, scalars and assets. This metadata can be used to retrieve
    samples, capsules for a particular time range.

    Parameters
    ----------
    query : {dict, list, pd.DataFrame, pd.Series}
        A mapping of property / match-criteria pairs.

        If you supply a dict or list of dicts, then the matching
        operations are "contains" (instead of "equal to").

        If you supply a DataFrame or a Series, then the matching
        operations are "equal to" (instead of "contains").

        'Name' and 'Description' fields support wildcard and regular expression
        (regex) matching with the same syntax as within the Data tab in Seeq
        Workbench.

        The 'Path' field allows you to query within an asset tree, where >>
        separates each level from the next. E.g.: 'Path': 'Example >> Cooling*'
        You can use wildcard and regular expression matching at any level but,
        unlike the Name/Description fields, the match must be a "full match",
        meaning that 'Path': 'Example' will match on a root asset tree node of
        'Example' but not 'Example (AF)'.

        Available options are:

        =================== ===================================================
        Property            Description
        =================== ===================================================
        Name                Name of the item (wildcards/regex supported)
        Path                Asset tree path of the item
        Type                The item type. One of 'Signal', 'Condition',
                              'Scalar', 'Asset', 'Chart', 'Metric', 'Workbook',
                              and 'Worksheet'
        Description         Description of the item (wildcards/regex supported)
        Datasource Name     Name of the datasource
        Datasource ID       The datasource ID
        Datasource Class    The datasource class (e.g. 'OSIsoft PI')
        Cache Enabled       True to find items where data caching is enabled
        Scoped To           The Seeq ID of a workbook such that results are
                              limited to ONLY items scoped to that workbook.
        =================== ===================================================


    all_properties : bool, default False
        True if all item properties should be retrieved. This currently makes
        the search operation much slower as retrieval of properties for an item
        requires a separate call.

    workbook : {str, None}
        A path string (with ' >> ' delimiters) or an ID to indicate a workbook
        such that, in addition to globally-scoped items, the workbook's scoped
        items will also be returned in the results.

        If you don't want globally-scoped items in your results, use the
        'Scoped To' field in the 'query' argument instead. (See 'query'
        argument documentation above.)

        The ID for a workbook is visible in the URL of Seeq Workbench, directly
        after the "workbook/" part.

    recursive : bool, default True
        If True, searches that include a Path entry will include items at and
        below the specified location in an asset tree. If False, then only
        items at the specified level will be returned. To get only the root
        assets, supply a Path value of ''.

    include_archived : bool, default False
        If True, includes trashed/archived items in the output.

    quiet : bool, default False
        If True, suppresses progress output.

    status : spy.Status, optional
        If supplied, this Status object will be updated as the command
        progresses.

    Returns
    -------
    pandas.DataFrame
        A DataFrame with rows for each item found and columns for each
        property.

    Examples
    --------
    Search for signals with the name 'Humid' on the asset tree under
    'Example >> Cooling Tower 1', retrieving all properties on the results:

    >>> spy.search({'Name': 'Humid', 'Path': 'Example >> Cooling Tower 1'}, all_properties=True)

    Using a pandas.DataFrame as the input:

    >>> my_items = pd.DataFrame(
    >>>     {'Name': ['Area A_Temperature', 'Area B_Compressor Power', 'Optimize' ],
    >>>      'Datasource Name': 'Example Data'})
    >>> spy.search(my_items)
    """
    _common.validate_argument_types([
        (query, 'query', (dict, list, pd.DataFrame, pd.Series)),
        (all_properties, 'all_properties', bool),
        (workbook, 'workbook', str),
        (recursive, 'recursive', bool),
        (include_archived, 'include_archived', bool),
        (quiet, 'quiet', bool),
        (status, 'status', _common.Status)
    ])

    _login.validate_login()

    status = Status.validate(status, quiet)
    try:
        return _search(query, all_properties=all_properties, workbook=workbook, recursive=recursive,
                       include_archived=include_archived, quiet=quiet, status=status)

    except KeyboardInterrupt:
        status.update('Search canceled', Status.CANCELED)


def _search(query, *, all_properties=False, workbook=_common.DEFAULT_WORKBOOK_PATH, recursive=True,
            include_archived=False, quiet=False, status=None):
    status = Status.validate(status, quiet)

    if not recursive and 'Path' not in query:
        raise ValueError("'Path' must be included in query when recursive=False")

    items_api = ItemsApi(_login.client)
    trees_api = TreesApi(_login.client)
    signals_api = SignalsApi(_login.client)
    conditions_api = ConditionsApi(_login.client)
    scalars_api = ScalarsApi(_login.client)

    if isinstance(query, pd.DataFrame):
        queries = query.to_dict(orient='records')
        comparison = '=='
    elif isinstance(query, pd.Series):
        queries = [query.to_dict()]
        comparison = '=='
    elif isinstance(query, list):
        queries = query
        comparison = '~='
    else:
        queries = [query]
        comparison = '~='

    #
    # This function makes use of a lot of inner function definitions that utilize variables from the outer scope.
    # In order to keep things straight, all variables confined to the inner scope are prefixed with an underscore.
    #

    metadata = list()
    columns = list()
    warnings = set()
    ids = set()
    dupe_count = 0

    status.df = pd.DataFrame(queries)
    status.df['Time'] = 0
    status.df['Count'] = 0
    status.df['Result'] = 'Queued'
    status.update('Initializing', Status.RUNNING)

    def _add_to_dict(_dict, _key, _val):
        if _key in ['Archived', 'Cache Enabled']:
            _val = bool(_val)
        _dict[_key] = _common.none_to_nan(_val)

        # We want the columns to appear in a certain order (the order we added them in) for readability
        if _key not in columns:
            columns.append(_key)

    def _add_to_metadata(_prop_dict):
        if _prop_dict['ID'] not in ids:
            metadata.append(_prop_dict)
            ids.add(_prop_dict['ID'])
        else:
            nonlocal dupe_count
            dupe_count += 1

    def _get_warning_string():
        if len(warnings) == 0:
            return ''

        return '\nWarning(s):\n' + '\n'.join(warnings)

    def _add_all_properties(_id, _prop_dict):
        _item = items_api.get_item_and_all_properties(id=_id)  # type: ItemOutputV1
        for _prop in _item.properties:  # type: PropertyOutputV1
            _add_to_dict(_prop_dict, _prop.name, _prop.value)

        # Name and Type don't seem to appear in additional properties
        _add_to_dict(_prop_dict, 'Name', _item.name)
        _add_to_dict(_prop_dict, 'Type', _item.type)
        _add_to_dict(_prop_dict, 'Scoped To', _common.none_to_nan(_item.scoped_to))

        if _item.type == 'CalculatedSignal':
            _signal_output = signals_api.get_signal(id=_item.id)  # type: SignalOutputV1
            _add_to_dict(_prop_dict, 'Formula Parameters', [
                '%s=%s' % (_p.name, _p.item.id if _p.item else _p.formula) for _p in _signal_output.parameters
            ])

        if _item.type == 'CalculatedCondition':
            _condition_output = conditions_api.get_condition(id=_item.id)  # type: ConditionOutputV1
            _add_to_dict(_prop_dict, 'Formula Parameters', [
                '%s=%s' % (_p.name, _p.item.id if _p.item else _p.formula) for _p in _condition_output.parameters
            ])

        if _item.type == 'CalculatedScalar':
            _scalar_output = scalars_api.get_scalar(id=_item.id)  # type: CalculatedItemOutputV1
            _add_to_dict(_prop_dict, 'Formula Parameters', [
                '%s=%s' % (_p.name, _p.item.id if _p.item else _p.formula) for _p in _scalar_output.parameters
            ])

        return _prop_dict

    workbook_id = None
    if workbook:
        if _common.is_guid(workbook):
            workbook_id = _common.sanitize_guid(workbook)
        else:
            search_query, _ = _push.create_analysis_search_query(workbook)
            search_df = spy.workbooks.search(search_query, status=status.create_inner(quiet=True))
            workbook_id = search_df.iloc[0]['ID'] if len(search_df) > 0 else None

    datasource_ids = dict()

    for status_index in range(len(queries)):
        timer = _common.timer_start()

        current_query = queries[status_index]

        if _common.present(current_query, 'ID'):
            # If ID is specified, short-circuit everything and just get the item directly
            _add_to_metadata(_add_all_properties(current_query['ID'], dict()))
            continue

        # If the user wants a recursive search or there's no 'Path' in the query, then use the ItemsApi.search_items API
        use_search_items_api = recursive or not _common.present(current_query, 'Path')

        if not use_search_items_api and include_archived:
            # As you can see in the code below, the TreesApi.get_tree() API doesn't have the ability to request
            # archived items
            raise ValueError('include_archived=True can only be used with recursive searches or searches that do not '
                             'involve a Path parameter')

        allowed_properties = ['Type', 'Name', 'Description', 'Path', 'Asset', 'Datasource Class', 'Datasource ID',
                              'Datasource Name', 'Data ID', 'Cache Enabled', 'Scoped To']

        for key, value in current_query.items():
            if key not in allowed_properties:
                warnings.add('Property "%s" is not an indexed property and will be ignored. Use any of the '
                             'following searchable properties and then filter further using DataFrame '
                             'operations:\n"%s"' % (key, '", "'.join(allowed_properties)))

        item_types = list()
        clauses = dict()

        if _common.present(current_query, 'Type'):
            item_type_specs = list()
            if isinstance(current_query['Type'], list):
                item_type_specs.extend(current_query['Type'])
            else:
                item_type_specs.append(current_query['Type'])

            valid_types = ['StoredSignal', 'CalculatedSignal',
                           'StoredCondition', 'CalculatedCondition',
                           'StoredScalar', 'CalculatedScalar',
                           'Datasource', 'TableDatasource',
                           'ThresholdMetric', 'Chart', 'Asset',
                           'Workbook', 'Worksheet']

            for item_type_spec in item_type_specs:
                if item_type_spec == 'Signal':
                    item_types.extend(['StoredSignal', 'CalculatedSignal'])
                elif item_type_spec == 'Condition':
                    item_types.extend(['StoredCondition', 'CalculatedCondition'])
                elif item_type_spec == 'Scalar':
                    item_types.extend(['StoredScalar', 'CalculatedScalar'])
                elif item_type_spec == 'Datasource':
                    item_types.extend(['Datasource', 'TableDatasource'])
                elif item_type_spec == 'Metric':
                    item_types.extend(['ThresholdMetric'])
                elif item_type_spec not in valid_types:
                    raise ValueError(f'Type field value not recognized: {item_type_spec}\n'
                                     f'Valid types: {", ".join(valid_types)}')
                else:
                    item_types.append(item_type_spec)

            del current_query['Type']

        for prop_name in ['Name', 'Description', 'Datasource Class', 'Datasource ID', 'Data ID']:
            if prop_name in current_query and not pd.isna(current_query[prop_name]):
                clauses[prop_name] = (comparison, current_query[prop_name])

        if _common.present(current_query, 'Datasource Name'):
            datasource_name = _common.get(current_query, 'Datasource Name')
            if datasource_name in datasource_ids:
                clauses['Datasource ID'], clauses['Datasource Class'] = datasource_ids[datasource_name]
            else:
                _filters = ['Name == %s' % datasource_name]
                if _common.present(current_query, 'Datasource ID'):
                    _filters.append('Datasource ID == %s' % _common.get(current_query, 'Datasource ID'))
                if _common.present(current_query, 'Datasource Class'):
                    _filters.append('Datasource Class == %s' % _common.get(current_query, 'Datasource Class'))

                _filter_list = [' && '.join(_filters)]
                if include_archived:
                    _filter_list.append('@includeUnsearchable')

                datasource_results = items_api.search_items(filters=_filter_list,
                                                            types=['Datasource'],
                                                            limit=100000)  # type: ItemSearchPreviewPaginatedListV1

                if len(datasource_results.items) > 1:
                    raise RuntimeError(
                        'Multiple datasources found that match "%s"' % datasource_name)
                elif len(datasource_results.items) == 0:
                    raise RuntimeError(
                        'No datasource found that matches "%s"' % datasource_name)
                else:
                    datasource = datasource_results.items[0]  # type: ItemSearchPreviewV1
                    clauses['Datasource ID'] = ('==', items_api.get_property(id=datasource.id,
                                                                             property_name='Datasource ID').value)
                    clauses['Datasource Class'] = ('==', items_api.get_property(id=datasource.id,
                                                                                property_name='Datasource Class').value)

                datasource_ids[datasource_name] = (clauses['Datasource ID'], clauses['Datasource Class'])

            del current_query['Datasource Name']

        filters = list()
        if len(clauses.items()) > 0:
            filters.append(' && '.join([p + c + v for p, (c, v) in clauses.items()]))

        if include_archived:
            filters.append('@includeUnsearchable')

        kwargs = {
            'filters': filters,
            'types': item_types,
            'limit': _config.options.search_page_size
        }

        if workbook:
            if workbook_id:
                kwargs['scope'] = workbook_id
            elif workbook != _common.DEFAULT_WORKBOOK_PATH:
                raise RuntimeError('Workbook "%s" not found, or is not accessible by you' % workbook)

        if _common.present(current_query, 'Scoped To'):
            kwargs['scope'] = current_query['Scoped To']
            kwargs['filters'].append('@excludeGloballyScoped')

        if _common.present(current_query, 'Asset') and not _common.present(current_query, 'Path'):
            raise ValueError('"Path" query parameter must be present when "Asset" parameter present')

        path_to_query = None
        if _common.present(current_query, 'Path'):
            path_to_query = current_query['Path']
            if _common.present(current_query, 'Asset'):
                path_to_query = path_to_query + ' >> ' + current_query['Asset']

        def _do_search(_offset):
            kwargs['offset'] = _offset

            if use_search_items_api:
                return items_api.search_items(**kwargs)
            else:
                _kwargs2 = {
                    'offset': kwargs['offset'],
                    'limit': kwargs['limit']
                }

                if 'scope' in kwargs:
                    _kwargs2['scoped_to'] = kwargs['scope']

                if 'asset' in kwargs:
                    _kwargs2['id'] = kwargs['asset']

                    return trees_api.get_tree(**_kwargs2)
                else:
                    return trees_api.get_tree_root_nodes(**_kwargs2)

        def _iterate_over_output(_output_func, _collection_name, _action_func):
            _offset = 0
            while True:
                _output = _output_func(_offset)

                _collection = getattr(_output, _collection_name)

                status.df.at[status_index, 'Time'] = _common.timer_elapsed(timer)
                status.df.at[status_index, 'Count'] = _offset + len(_collection)
                status.df.at[status_index, 'Result'] = 'Querying'
                status.update('Querying Seeq Server for items' + _get_warning_string(), Status.RUNNING)

                for _item in _collection:
                    _action_func(_item)

                if len(_collection) != _output.limit:
                    break

                _offset += _output.limit

            status.df.at[status_index, 'Result'] = 'Success'

        def _gather_results(_actual_path_list=None):
            def _gather_results_via_item_search(_result):
                _item_search_preview = _result  # type: ItemSearchPreviewV1
                _prop_dict = dict()

                _add_to_dict(_prop_dict, 'ID', _item_search_preview.id)
                if len(_item_search_preview.ancestors) > 1:
                    _add_to_dict(_prop_dict, 'Path',
                                 _common.path_list_to_string([_a.name for _a in _item_search_preview.ancestors[0:-1]]))
                    _add_to_dict(_prop_dict, 'Asset', _item_search_preview.ancestors[-1].name)
                elif len(_item_search_preview.ancestors) == 1:
                    _add_to_dict(_prop_dict, 'Path', np.nan)
                    _add_to_dict(_prop_dict, 'Asset', _item_search_preview.ancestors[0].name)

                _add_to_dict(_prop_dict, 'Name', _item_search_preview.name)
                _add_to_dict(_prop_dict, 'Description', _item_search_preview.description)
                _add_to_dict(_prop_dict, 'Type', _item_search_preview.type)
                _uom = _item_search_preview.value_unit_of_measure if _item_search_preview.value_unit_of_measure \
                    else _item_search_preview.source_value_unit_of_measure
                _add_to_dict(_prop_dict, 'Value Unit Of Measure', _uom)
                _datasource_item_preview = _item_search_preview.datasource  # type: ItemPreviewV1
                _add_to_dict(_prop_dict, 'Datasource Name',
                             _datasource_item_preview.name if _datasource_item_preview else None)
                _add_to_dict(_prop_dict, 'Archived', _item_search_preview.is_archived)
                if all_properties:
                    _add_all_properties(_item_search_preview.id, _prop_dict)

                _add_to_metadata(_prop_dict)

            def _gather_results_via_get_tree(_result):
                _tree_item_output = _result  # type: TreeItemOutputV1
                _prop_dict = dict()

                for _prop, _attr in [('Name', 'name'), ('Description', 'description')]:
                    if _prop not in current_query:
                        continue

                    if not _common.does_query_fragment_match(current_query[_prop],
                                                             getattr(_tree_item_output, _attr),
                                                             contains=(comparison == '~=')):
                        return

                _add_to_dict(_prop_dict, 'ID', _tree_item_output.id)
                if len(_actual_path_list) > 1:
                    _add_to_dict(_prop_dict, 'Path', _common.path_list_to_string(_actual_path_list[0:-1]))
                    _add_to_dict(_prop_dict, 'Asset', _actual_path_list[-1])
                elif len(_actual_path_list) == 1:
                    _add_to_dict(_prop_dict, 'Path', np.nan)
                    _add_to_dict(_prop_dict, 'Asset', _actual_path_list[0])

                _add_to_dict(_prop_dict, 'Name', _tree_item_output.name)
                _add_to_dict(_prop_dict, 'Description', _tree_item_output.description)
                _add_to_dict(_prop_dict, 'Type', _tree_item_output.type)
                _add_to_dict(_prop_dict, 'Value Unit Of Measure', _tree_item_output.value_unit_of_measure)
                _add_to_dict(_prop_dict, 'Archived', _tree_item_output.is_archived)

                if all_properties:
                    _add_all_properties(_tree_item_output.id, _prop_dict)

                _add_to_metadata(_prop_dict)

            if use_search_items_api:
                _iterate_over_output(_do_search, 'items', _gather_results_via_item_search)
            else:
                _iterate_over_output(_do_search, 'children', _gather_results_via_get_tree)

        if not _common.present(current_query, 'Path'):
            # If there's no 'Path' property in the query, we can immediately proceed to the results gathering stage.
            _gather_results()
        else:
            # If there is a 'Path' property in the query, then first we have to drill down through the tree to the
            # appropriate depth so we can find the asset ID to use for the results gathering stage.

            # We define a function here so we can use recursion through the path.
            def _process_query_path_string(_remaining_query_path_string, _actual_path_list, _asset_id=None):
                _query_path_list = _common.path_string_to_list(_remaining_query_path_string)

                _query_path_part = _query_path_list[0]

                _tree_kwargs = dict()
                _tree_kwargs['limit'] = kwargs['limit']
                _tree_kwargs['offset'] = 0

                if 'scope' in kwargs:
                    _tree_kwargs['scoped_to'] = kwargs['scope']

                while True:
                    if not _asset_id:
                        _tree_output = trees_api.get_tree_root_nodes(**_tree_kwargs)  # type: AssetTreeOutputV1
                    else:
                        _tree_kwargs['id'] = _asset_id
                        _tree_output = trees_api.get_tree(**_tree_kwargs)  # type: AssetTreeOutputV1

                    for _child in _tree_output.children:  # type: TreeItemOutputV1
                        if not _asset_id:
                            # We only filter out datasource at the top level, in case the tree is mixed
                            _datasource_ok = True
                            _child_item_output = items_api.get_item_and_all_properties(
                                id=_child.id)  # type: ItemOutputV1
                            for _prop in ['Datasource Class', 'Datasource ID']:
                                if _prop in clauses:
                                    _, _val = clauses[_prop]
                                    _p_list = [_p.value for _p in _child_item_output.properties if
                                               _p.name == _prop]
                                    if len(_p_list) == 0 or _p_list[0] != _val:
                                        _datasource_ok = False

                            if not _datasource_ok:
                                continue

                        if _common.does_query_fragment_match(_query_path_part, _child.name, contains=False):
                            _actual_path_list_for_child = _actual_path_list.copy()
                            _actual_path_list_for_child.append(_child.name)
                            if len(_query_path_list) == 1:
                                kwargs['asset'] = _child.id
                                _gather_results(_actual_path_list_for_child)
                            else:
                                _process_query_path_string(_common.path_list_to_string(_query_path_list[1:]),
                                                           _actual_path_list_for_child,
                                                           _child.id)

                    if len(_tree_output.children) < _tree_kwargs['limit']:
                        break

                    _tree_kwargs['offset'] += _tree_kwargs['limit']

            if len(path_to_query) == 0:
                _gather_results(list())
            else:
                _process_query_path_string(path_to_query, list())

    if dupe_count > 0:
        warnings.add(f'{dupe_count} duplicates removed from returned DataFrame.')

    status.update('Query successful' + _get_warning_string(), Status.SUCCESS)

    return pd.DataFrame(data=metadata, columns=columns)
