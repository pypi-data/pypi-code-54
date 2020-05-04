from rest_framework.views import APIView

from django.http import JsonResponse
from django.utils.translation import get_language_from_request

from cms.utils.page import get_page_from_request
from cms.models.pagemodel import Page

from .utils import (get_plugin_info, get_title_info)


class AllPagesView(APIView):
    def get(self, request, **kwargs):
        request_language = get_language_from_request(request, check_path=True)
        pages_list = Page.objects.filter(publisher_is_draft=0)
        pages_list_query_set = pages_list.values()

        response = {}
        response['meta'] = {
            'language': request_language
        }
        response['body'] = []

        for index, page in enumerate(list(pages_list_query_set)):
            response['body'].insert(index, page)
            response['body'][index]['title'] = get_title_info(pages_list[index], request_language)
        return JsonResponse(response, safe=False)


class PageDetails(APIView):
    def get(self, request, **kwargs):
        page = get_page_from_request(request, kwargs.get('path', ''))
        request_language = get_language_from_request(request, check_path=True)
        all_placeholders = page.get_placeholders()
        response = {}
        response['meta'] = {
            'language': request_language
        }
        response['title'] = get_title_info(page, request_language)
        response['body'] = []
        for index, placeholder in enumerate(list(all_placeholders.values())):
            print(type(all_placeholders[index]))
            response['body'].insert(index, placeholder)
            response['body'][index]['data'] = get_plugin_info(all_placeholders[index].get_plugins_list())
        return JsonResponse(response, safe=False)
