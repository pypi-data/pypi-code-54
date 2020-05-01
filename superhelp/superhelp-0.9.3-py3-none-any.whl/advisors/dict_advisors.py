from ..advisors import filt_block_advisor
from .. import code_execution, conf, utils
from ..ast_funcs import get_assign_name
from ..utils import get_nice_str_list, layout_comment as layout

ASSIGN_DICT_XPATH = 'descendant-or-self::Assign/value/Dict'

def _get_detailed_list_comment(first_name):
    additional_main_msg = (
        layout(f"""

            It is common to iterate through the key-value pairs of a dictionary.
            This can be achieved using the dictionary's `.items()` method. E.g.

            """)
        +
        layout(f"""\
            ## k, v is conventional, and OK in a hurry, but readable names
            ## are probably better for code you're going to maintain
            for k, v in {first_name}.items():
                print(f"key {{k}} maps to value {{v}}")
            """, is_code=True)
        +
        layout(f"""
            
            Keys are unique but values can be repeated. For example:

            """)
        +
        layout(f"""
            country2car = {{'Japan': 'Toyota', 'Sweden': 'Volvo'}}  ## OK - all keys are unique
            country2car = {{'Japan': 'Toyota', 'Japan': 'Honda'}}  ## Oops - the 'Japan' key is repeated

            """, is_code=True)
        +
        layout(f"""

            In which case a better structure might be to have each 'value'
            being a list e.g.

            """)
        +
        layout(f"""
            country2cars = {{'Japan': ['Toyota', 'Honda'], 'Sweden': ['Volvo']}}  ## OK - all keys are unique

            """, is_code=True)
    )
    return additional_main_msg

def _get_minimal_dict_details(block_dets, dict_els, plural):
    brief_msg = ''
    for i, dict_el in enumerate(dict_els):
        first = (i == 0)
        name = get_assign_name(dict_el)
        items = code_execution.get_val(
            block_dets.pre_block_code_str, block_dets.block_code_str, name)
        if first:
            title = layout(f"""\

                ### Dictionar{plural} defined

                """)
            brief_msg += title
        brief_msg += layout(f"""\

            `{name}` is a dictionary with {utils.int2nice(len(items))} items
            (i.e. {utils.int2nice(len(items))} mappings).
            """)
    message = {
        conf.BRIEF: brief_msg,
    }
    return message

def _get_full_dict_details(block_dets, dict_els, plural):
    brief_msg = ''
    main_msg = ''
    first_name = None
    for i, dict_el in enumerate(dict_els):
        first = (i == 0)
        name = get_assign_name(dict_el)
        items = code_execution.get_val(
            block_dets.pre_block_code_str, block_dets.block_code_str, name)
        if first:
            first_name = name
            title = layout(f"""\

                ### Dictionar{plural} defined

                """)
            brief_msg += title
            main_msg += title

            brief_msg += layout("""\

                Dictionaries map keys to values.

                """)
            main_msg += layout("""\

                Dictionaries, along with lists, are the workhorses of Python
                data structures.

                """)
        empty_dict = (len(items) == 0)
        if empty_dict:
            list_desc = layout(f"""\

                `{name}` is an empty dictionary.

                """)
        else:
            plural = '' if len(items) == 1 else 's'
            list_desc = layout(f"""\

                `{name}` is a dictionary with {utils.int2nice(len(items))}
                item{plural} (i.e. {utils.int2nice(len(items))}
                mapping{plural}). In this case, the keys are:
                {list(items.keys())}. We can get the keys using the `.keys()`
                method e.g. `{name}`.`keys()`. The values are
                {list(items.values())}. We can get the values using the
                `.values()` method e.g. `{name}`.`values()`.

                """)
        brief_msg += list_desc
        main_msg += list_desc
   
        brief_msg += layout("""\

            Keys are unique but values can be repeated.

            Dictionaries, along with lists, are the workhorses of Python data
            structures.
            """)
    main_msg += _get_detailed_list_comment(first_name)
    message = {
        conf.BRIEF: brief_msg,
        conf.MAIN: main_msg,
        conf.EXTRA: layout("""\

            Python dictionaries (now) keep the order in which items are added.

            They are also super-efficient and fast. The two presentations to
            watch are by living treasure Brandon Rhodes:

            1. The Dictionary Even Mightier -
            <https://www.youtube.com/watch?v=66P5FMkWoVU>
            2. The Mighty Dictionary -
            <https://www.youtube.com/watch?v=oMyy4Sm0uBs>
            """)
    }
    return message

@filt_block_advisor(xpath=ASSIGN_DICT_XPATH)
def dict_overview(block_dets, *, repeated_message=False):
    """
    Look at assigned dictionaries e.g. location = {'country' 'New Zealand',
    'city': 'Auckland'}
    """
    dict_els = block_dets.element.xpath(ASSIGN_DICT_XPATH)
    plural = 'ies' if len(dict_els) > 1 else 'y'
    if repeated_message:
        message = _get_minimal_dict_details(block_dets, dict_els, plural)
    else:
        message = _get_full_dict_details(block_dets, dict_els, plural)
    return message

def get_key_type_names(items):
    key_type_names = sorted(set(
        [type(item).__name__ for item in items]
    ))
    key_type_nice_names = [
        conf.TYPE2NAME.get(key_type, key_type)
        for key_type in key_type_names]
    return key_type_names, key_type_nice_names

@filt_block_advisor(xpath=ASSIGN_DICT_XPATH, warning=True)
def mixed_key_types(block_dets, *, repeated_message=False):
    """
    Warns about dictionaries with mix of string and integer keys.
    """
    dict_els = block_dets.element.xpath(ASSIGN_DICT_XPATH)
    brief_msg = ''
    main_msg = ''
    has_mixed = False
    mixed_names = []
    for i, dict_el in enumerate(dict_els):
        first = (i == 0)
        name = get_assign_name(dict_el)
        items = code_execution.get_val(
            block_dets.pre_block_code_str, block_dets.block_code_str, name)
        key_type_names, _key_type_nice_names = get_key_type_names(items)
        bad_key_type_combo = (
            conf.INT_TYPE in key_type_names and conf.STR_TYPE in key_type_names)
        if not bad_key_type_combo:
            continue
        mixed_names.append(name)
        has_mixed = True
        if first:
            title = layout(f"""\

                ### Mix of integer and string keys in dictionary

                """)
            brief_msg += title
            main_msg += title
    if not has_mixed:
        return None
    multiple = len(mixed_names) > 1
    if multiple:
        nice_str_list = get_nice_str_list(mixed_names, quoter='`')
        mixed_warning = layout(f"""

            {nice_str_list} have keys include a mix of strings and integers -
            which is probably a bad idea.
            """)
    else:
        mixed_warning = layout(f"""

            `{name}`'s keys include both strings and integers which is probably
            a bad idea.
            """)
    brief_msg += mixed_warning
    main_msg += mixed_warning

    if not repeated_message:
        main_msg += layout("""\

            For example, if you have both 1 and "1" as keys in a dictionary
            (which is allowed because they are not the same key) it is very easy
            to get confused and create Hard To Find™ bugs. You _might_ not
            regret it but you probably will ;-).
            """)

    message = {
        conf.BRIEF: brief_msg,
        conf.MAIN: main_msg,
    }
    return message
