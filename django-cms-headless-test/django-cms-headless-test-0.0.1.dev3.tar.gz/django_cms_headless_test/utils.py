from collections import defaultdict
from cms.plugin_pool import plugin_pool

def get_plugin_info(plugins):
    plugin_types_map = defaultdict(list)
    plugin_ids = []
    for plugin in plugins:
        plugin_ids.append(plugin.pk)
        plugin_types_map[plugin.plugin_type].append(plugin.pk)
    plugin_qs = []
    tempArray = []
    for plugin_type, pks in plugin_types_map.items():
        cls = plugin_pool.get_plugin(plugin_type)
        plugin_qs = cls.get_render_queryset().filter(pk__in=pks)
        for p_list in plugin_qs.values():
            p_list['children'] = []
            tempArray.append(p_list)
    return get_structured_content(tempArray)


def get_structured_content(tempArray):
    tempArray = sorted(tempArray, key=lambda i: i['depth'], reverse=True)
    n = []
    for value in tempArray:
        if value['parent_id'] is None:
            n.insert(value['position'], value)
        else:
            parent = value['parent_id']
            index = find(tempArray, 'id', parent)
            tempArray[index]['children'].insert(value['position'], value)
            print("index")
            print(index)
    return n


def find(lst, key, value):
    for i, dic in enumerate(lst):
        if dic[key] == value:
            return i
    return -1

def get_title_info(page, request_language):
    return {
        'title': page.get_title(request_language),
        'path': page.get_path(request_language),
        'slug': page.get_slug(request_language),
        'menu_title': page.get_menu_title(request_language),
        'page_title': page.get_page_title(request_language),
    }