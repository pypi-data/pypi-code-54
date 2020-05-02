from rest_framework.views import APIView
from django.http import HttpResponse, JsonResponse
from django.core import serializers

from cms.utils.page import get_page_from_request
from django.utils.translation import get_language_from_request
from cms.utils.plugins import assign_plugins
from collections import defaultdict
from cms.plugin_pool import plugin_pool
from cms.models.pagemodel import Page


class AllPagesView(APIView):
    def get(self, request, **kwargs):
        request_language = get_language_from_request(request, check_path=True)
        pagesList = Page.objects.filter(publisher_is_draft=0)
        pagesListQuerySet = pagesList.values()
        pagesListDict = list(pagesListQuerySet)
        response = {}
        response['meta'] = {
            'language': request_language 
        }
        response['body'] = []
        for index, page in enumerate(pagesListDict):
            response['body'].insert(index, page)
            p = pagesList[index]
            response['body'][index]['title'] = {
            'title': p.get_title(request_language),
            'menu_title': p.get_menu_title(request_language),
            'path': p.get_path(request_language),
            'slug': p.get_slug(request_language),
            'page_title': p.get_page_title(request_language),
        }
        return JsonResponse(response, safe=False)


class PageDetails(APIView):
    def get(self, request, **kwargs):
        page = get_page_from_request(request, kwargs.get('path', ''))
        request_language = get_language_from_request(request, check_path=True)
        allPlaceholdersForPage = page.get_placeholders()
        allPlaceholdersForPageQuerySet = allPlaceholdersForPage.values()
        allPlaceholdersForPageList = list(allPlaceholdersForPageQuerySet)
        response = {}
        response['meta'] = {
            'language': request_language
        }
        response['title'] = {
            'title': page.get_title(request_language),
            'menu_title': page.get_menu_title(request_language),
            'path': page.get_path(request_language),
            'slug': page.get_slug(request_language),
            'page_title': page.get_page_title(request_language),
        }
        temp = []
        for index, placeholder in enumerate(allPlaceholdersForPageList):
            print(type(allPlaceholdersForPage[index]))
            temp.insert(index, placeholder)
            data = downcast_plugins(allPlaceholdersForPage[index].get_plugins_list())
            temp[index]['data'] = data
        response['body'] = temp        
        return JsonResponse(response, safe=False)


def dump(obj):
    count = 0
    for attr in dir(obj):
        if hasattr( obj, attr ):
            print( "obj.%s = %s" % (attr, getattr(obj, attr)))
            print(count)
            count = count + 1
            print('')

def downcast_plugins(plugins):
    plugin_types_map = defaultdict(list)
    plugin_lookup = {}
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