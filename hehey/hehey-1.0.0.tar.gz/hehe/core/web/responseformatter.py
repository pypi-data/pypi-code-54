from abc import abstractmethod,ABCMeta
import json

class ResponseFormatter(object):

    def __init__(self):

        self.contentType = '';

    @abstractmethod
    def format(self,response):

        pass


class HtmlResponseFormatter(ResponseFormatter):

    def __init__(self):

        self.contentType = '';

    def format(self,response):
        """

        :param response:
        :type response:hehe.core.web.WebResponse.WebResponse
        :return:
        """

        response.contentType = 'text/html'
        if response.content:
            response.content = response.content.encode('utf-8')

        return ;

class RawResponseFormatter(ResponseFormatter):

    def __init__(self):

        self.contentType = '';

    def format(self,response):
        """

        :param response:
        :type response:hehe.core.web.WebResponse.WebResponse
        :return:
        """

        #response.contentType = 'text/html'

        return ;


class JsonResponseFormatter(ResponseFormatter):


    def format(self,response):
        """
        :param response:
        :type response:hehe.core.web.WebResponse.WebResponse
        :return:
        """

        response.contentType = 'application/json; charset=UTF-8'
        response.content = json.dumps(response.content)
        response.content = response.content.encode('utf-8')

        return ;