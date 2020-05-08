# -*- coding: utf-8 -*-
from .Cookies import Cookies
from .Headers import Headers
from ..base.Response import Response
from hehe.helper.ClassHelper import ClassHelper
from hehe import he
import os,re,types
import mimetypes
from inspect import isfunction


"""
 *框架流程控制类
 *<B>说明：</B>
 *<pre>
 *  略
 *</pre>
 *<B>示例：</B>
 *<pre>
 *  略
 *</pre>
 *<B>日志：</B>
 *<pre>
 *  略
 *</pre>
 *<B>注意事项：</B>
 *<pre>
 *  略
 *</pre>
"""

class WebResponse(Response):

    '''
    :type cookies: hehe.core.base.Cookies.Cookies

    '''

    FORMAT_RAW = 'raw';
    FORMAT_HTML = 'html';
    FORMAT_JSON = 'json';
    FORMAT_JSONP = 'jsonp';
    FORMAT_XML = 'xml';

    # http 状态码列表
    httpStatuses = {
        '100': 'Continue',
        '101': 'Switching Protocols',
        '102': 'Processing',
        '118': 'Connection timed out',
        '200': 'OK',
        '201': 'Created',
        '202': 'Accepted',
        '203': 'Non-Authoritative',
        '204': 'No Content',
        '205': 'Reset Content',
        '206': 'Partial Content',
        '207': 'Multi-Status',
        '208': 'Already Reported',
        '210': 'Content Different',
        '226': 'IM Used',
        '300': 'Multiple Choices',
        '301': 'Moved Permanently',
        '302': 'Found',
        '303': 'See Other',
        '304': 'Not Modified',
        '305': 'Use Proxy',
        '306': 'Reserved',
        '307': 'Temporary Redirect',
        '308': 'Permanent Redirect',
        '310': 'Too many Redirect',
        '400': 'Bad Request',
        '401': 'Unauthorized',
        '402': 'Payment Required',
        '403': 'Forbidden',
        '404': 'Not Found',
        '405': 'Method Not Allowed',
        '406': 'Not Acceptable',
        '407': 'Proxy Authentication Required',
        '408': 'Request Time-out',
        '409': 'Conflict',
        '410': 'Gone',
        '411': 'Length Required',
        '412': 'Precondition Failed',
        '413': 'Request Entity Too Large',
        '414': 'Request-URI Too Long',
        '415': 'Unsupported Media Type',
        '416': 'Requested range unsatisfiable',
        '417': 'Expectation failed',
        '418': 'I\'m a teapot',
        '422': 'Unprocessable entity',
        '423': 'Locked',
        '424': 'Method failure',
        '425': 'Unordered Collection',
        '426': 'Upgrade Required',
        '428': 'Precondition Required',
        '429': 'Too Many Requests',
        '431': 'Request Header Fields Too Large',
        '449': 'Retry With',
        '450': 'Blocked by Windows Parental Controls',
        '500': 'Internal Server Error',
        '501': 'Not Implemented',
        '502': 'Bad Gateway or Proxy Error',
        '503': 'Service Unavailable',
        '504': 'Gateway Time-out',
        '505': 'HTTP Version not supported',
        '507': 'Insufficient storage',
        '508': 'Loop Detected',
        '509': 'Bandwidth Limit Exceeded',
        '510': 'Not Extended',
        '511': 'Network Authentication Required',
    }

    formatters = {}

    def __init__(self):

        # 响应原始内容
        # <B> 说明： </B>
        # <pre>
        # 略
        # </pre>
        self.content = ''

        # 编码
        # <B> 说明： </B>
        # <pre>
        # 略
        # </pre>
        self.contentType = '';

        # 编码
        # <B> 说明： </B>
        # <pre>
        # 略
        # </pre>
        self.charset = '';

        # 状态码
        # <B> 说明： </B>
        # <pre>
        # 略
        # </pre>
        self.statusCode = 200;

        # 状态码文本
        # <B> 说明： </B>
        # <pre>
        # 略
        # </pre>
        self.statusText = 'OK'

        # http 版本文本
        # <B> 说明： </B>
        # <pre>
        # 略
        # </pre>
        self.version = '1.0'

        # cookies 对象
        # <B> 说明： </B>
        # <pre>
        # 略
        # </pre>
        self._cookies = None

        # cookies 对象
        # <B> 说明： </B>
        # <pre>
        # 略
        # </pre>
        self._headers = None

        self.formatter = self.__class__.FORMAT_HTML

        # 文件流内容
        # <B> 说明： </B>
        # <pre>
        # 略
        # </pre>
        self.streaming_content = None;

        return

    # 返回cookies 对象
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    def getCookies(self) -> 'Cookies':

        if self._cookies is None:
            self._cookies = Cookies()

        return self._cookies

    # 添加cookie
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    def addCookie(self,name,value = None,**params):

        self.getCookies().set(name,value,**params)

        return ;

    # 返回Headers对象
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    def getHeaders(self) -> 'Headers':

        if self._headers is None:
            self._headers = Headers()

        return self._headers

    # 设置整个headers
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    def setHeaders(self, headers):

        return self.getHeaders().setHeaders(headers);

    # 设置header
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    def setHeader(self,name,value):

        return self.getHeaders().set(name,value);

    # 追加header
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    def appendHeader(self, name, value):

        return self.getHeaders().append(name,value);

    # 设置状态码
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    def setStatusCode(self,statusCode,statusText = None):

        self.statusCode = statusCode
        self.statusText = statusText;

        if not self.statusCode:
            self.statusCode = 200;

        if self.statusText is None:
            self.statusText = self.__class__.httpStatuses.get(str(self.statusCode),'');

        return ;

    # 构建状态码 http
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    def buildHttpStatus(self):

        return '{0} {1}'.format(self.statusCode,self.statusText)

    # 构建headers http
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    def buildHttpHeaders(self):

        headers = self.getHeaders().formatHeaders();
        headers = headers + self.getCookies().formatCookies()

        return headers;

    # 输出之前的准备工作
    # <B> 说明： </B>
    # <pre>
    # 主要是格式化数据
    # </pre>
    def _prepare(self):

        # 设置默认状态码
        if self.statusCode == 0:
            self.setStatusCode(200);

        # 格式化数据
        formatter = self._getFormatter(self.formatter);
        formatter.format(self)
        headers = self.getHeaders();
        if not headers.has('Content-Type'):
            headers.set('Content-Type', self.contentType)

        return ;


    # 向客户端发送数据
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    def send(self):

        self._prepare()

    # 获取客户端数据
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    def getContent(self):

        if self.streaming_content:
            return self.streaming_content;

        if self.content:

            return [self.content];

        return ''

    # 输出文件
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    def sendFile(self,filePath, attachmentName = None, options = {}):

        if not attachmentName:
            attachmentName = os.path.basename(filePath)

        options['mimeType'] = options.get('mimeType', mimetypes.guess_type(attachmentName)[0])

        if isinstance(filePath,str):
            # 文件类型
            handle = open(filePath, 'rb')
            filesize = os.path.getsize(handle.name);
            options['filesize'] = filesize
            self.sendStreamAsFile(handle, attachmentName, options)
        else:
            self.sendFileForGenerator(filePath,attachmentName,options);

        return self;

    # 输出文件元素内容
    # <B> 说明： </B>
    # <pre>
    # 不提供下载的方式
    # </pre>
    def sendRawFile(self,filePath, attachmentName = None, options = {}):

        if not attachmentName:
            attachmentName = os.path.basename(filePath)

        options['mimeType'] = options.get('mimeType', mimetypes.guess_type(attachmentName)[0])
        options['downloadheader'] = False;

        if isinstance(filePath, str):
            # 文件类型
            handle = open(filePath, 'rb')
            filesize = os.path.getsize(handle.name);
            options['filesize'] = filesize
            self.sendStreamAsFile(handle, attachmentName, options)
        else:
            self.sendFileForGenerator(filePath, attachmentName, options);

        return self;

    # 以迭代方法的方式输出流数据
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    def sendFileForGenerator(self,handle, attachmentName = None, options = {}):

        mimeType = options.get('mimeType', None)
        inline = options.get('inline', False)
        filesize = options.get('filesize', 0)

        self.streaming_content = GeneratorWrapper(handle);
        # 设置文件下载相关头部
        self.setDowaloadHeaders(attachmentName, mimeType, inline, filesize,options);

        return self;



    # 输出文件流
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    def sendStreamAsFile(self,handle, attachmentName = None, options = {}):

        chunk_size = options.get('chunk_size',1024 * 1024 * 1)
        del_status = options.get('del_status', False)
        mimeType = options.get('mimeType',None)
        inline = options.get('inline',False)
        filesize = options.get('filesize',0)

        # 指针位置恢复
        headers = self.getHeaders();
        http_range = self.getHttpRange(filesize)
        if http_range is False:
            headers.set('Content-Range', "bytes */{0}".format(filesize));
            raise Exception(416, 'requested range not satisfiable');

        if http_range is True:
            self.setStatusCode(200);
            # 文件读取迭代器
            self.streaming_content = FileWrapper(handle, chunk_size, del_status);
        elif isinstance(http_range,list):
            begin, end = http_range;
            self.setStatusCode(206);
            headers.set('Content-Range', "bytes {0}/{1}".format(begin - end, filesize));
            # http range 文件读取迭代器
            self.streaming_content = HttpRangeFileWrapper(handle, http_range, chunk_size, del_status);
        # 设置文件下载相关头部
        self.setDowaloadHeaders(attachmentName,mimeType,inline,filesize,options);

        return self;

    # 输出内容
    # <B> 说明： </B>
    # <pre>
    # 常用与execl 导出等等
    # </pre>
    def sendContentAsFile(self,content,attachmentName = None, options = {}):

        mimeType = options.get('mimeType', mimetypes.guess_type(attachmentName)[0])
        filesize = len(content);
        inline = options.get('inline', False)

        # 指针位置恢复
        headers = self.getHeaders();
        http_range = self.getHttpRange(filesize)
        if http_range is False:
            headers.set('Content-Range', "bytes */{0}".format(filesize));
            raise Exception(416, 'requested range not satisfiable');

        if http_range is True:
            self.setStatusCode(200);
            if isinstance(content,str):
                content = content.encode('utf-8')

            # 文件读取迭代器
            self.streaming_content = [content];
        elif isinstance(http_range, list):
            begin, end = http_range;
            self.setStatusCode(206);
            headers.set('Content-Range', "bytes {0}/{1}".format(begin - end, filesize));
            if isinstance(content, str):
                content = content.encode('utf-8')

            self.streaming_content = [content[begin:]];

        self.setDowaloadHeaders(attachmentName, mimeType, inline, filesize,options);

        return self;

    # 获取分段位置信息
    # <B> 说明： </B>
    # <pre>
    # 断点续传
    # </pre>
    def getHttpRange(self,fileSize):

        http_range = he.app.hrequest.server('HTTP_RANGE',None);

        if http_range is None or http_range == '-':
            return True

        matches = re.match(r'bytes=(\d*)-(\d*)', http_range, re.M | re.I)

        if not matches:
            return False

        if matches.group(1) == '':
            start = fileSize - int(matches.group(2))
            end = fileSize - 1
        elif matches.group(2) != '':
            start = int(matches.group(1))
            end = int(matches.group(2))
            if end >= fileSize:
                end = fileSize - 1;
        else:
            start = int(matches.group(1))
            end = fileSize - 1

        if start < 0 or start > end:
            return False
        else:
            return [start,end]



    # 设置下载文件头部
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    def setDowaloadHeaders(self,attachmentName, mimeType = None, inline = False, contentLength = None,options = {}):

        headers = self.getHeaders();
        if inline:
            disposition = 'inline'
        else:
            disposition = 'attachment'

        downloadheader = options.get("downloadheader",True);
        if downloadheader:
            headers.set('Pragma','public');
            headers.set('Accept-Ranges', 'bytes');
            headers.set('Expires', '0');
            headers.set('Cache-Control', 'must-revalidate, post-check=0, pre-check=0');
            headers.set('Content-Transfer-Encoding', 'binary');
            headers.set('Content-Disposition', '{0}; filename="{1}"'.format(disposition,attachmentName));

        if mimeType is not None:
            headers.set('Content-Type', mimeType);

        if not contentLength:
            headers.set('Content-Length', contentLength);

        self.formatter = self.__class__.FORMAT_RAW;

        return self


    # 获取输出格式对象
    # <B> 说明： </B>
    # <pre>
    # 主要是格式化数据
    # </pre>
    @classmethod
    def _getFormatter(cls,formatter):
        """
        :param formatter:
        :rtype: hehe.core.web.responseformatter.ResponseFormatter
        :return:
        """
        formatterObj = cls.formatters.get(formatter,None)

        if formatterObj is not None:
            return formatterObj

        formatters = {
            cls.FORMAT_HTML:__package__ + '.responseformatter.HtmlResponseFormatter',
            cls.FORMAT_RAW: __package__ + '.responseformatter.RawResponseFormatter',
            cls.FORMAT_JSON: __package__ + '.responseformatter.JsonResponseFormatter'
        }

        formatterClazz = formatters.get(formatter,None)
        formatterMeta = ClassHelper.getClassMeta(formatterClazz)
        cls.formatters[formatter] = formatterMeta();

        return cls.formatters.get(formatter);

    # 跳转页面
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    def redirect(self,url,statusCode = 302):

        uri = url;
        if he.app.hrequest.isPjax():
            self.setHeader('X-Pjax-Url',uri)
        elif he.app.hrequest.isAjax():
            self.setHeader('X-Redirect', uri)
        else :
            self.setHeader('Location', uri)

        self.setStatusCode(statusCode)

        return self;


"""
 * 文件迭代器
 *<B>说明：</B>
 *<pre>
 *  wsgi 文件输出结束后,自动调用colse 函数 关闭文件句柄
 *</pre>
"""
class FileWrapper:

    def __init__(self, handle, chunk_size = 8192,del_status = False):

        self.handle = handle
        self.chunk_size = chunk_size
        self.del_status = del_status


    def close(self):

        # 关闭句柄
        self.handle.close()
        # 是否删除文件
        if self.del_status:
            filepath = os.path.abspath(self.handle.name)
            os.remove(filepath)

        return ;

    def __iter__(self):

        self.handle.seek(0)

        return self

    def __next__(self):

        data = self.handle.read(self.chunk_size)
        if data:
            return data

        raise StopIteration

"""
 * 断点续传文件迭代器
 *<B>说明：</B>
 *<pre>
 *  wsgi 文件输出结束后,自动调用colse 函数 关闭文件句柄
 *</pre>
"""
class HttpRangeFileWrapper:

    def __init__(self, handle,http_range = [], chunk_size = 8192,del_status = False):

        self.handle = handle
        self.chunk_size = chunk_size
        self.del_status = del_status
        self.http_range = http_range

    def close(self):

        # 关闭句柄
        self.handle.close()
        # 是否删除文件
        if self.del_status:
            filepath = os.path.abspath(self.handle.name)
            os.remove(filepath)

        return ;

    def __iter__(self):

        self.handle.seek(0)

        return self


    def __next__(self):

        begin, end = self.http_range;
        self.handle.seek(begin);

        if begin + self.chunk_size > end:
            chunkSize = end - begin + 1
        else:
            chunkSize = self.chunk_size;

        data = self.handle.read(chunkSize)
        if data:
            # 指针移位
            self.http_range = [self.handle.tell(),end];
            return data

        raise StopIteration


"""
 * 迭代方法迭代器
 *<B>说明：</B>
 *<pre>
 *  wsgi 文件输出结束后,自动调用colse 函数 关闭文件句柄
 *</pre>
"""
class GeneratorWrapper:

    def __init__(self, handle):

        self.handle = handle

    def close(self):

        return ;

    def __iter__(self):

        return self

    def __next__(self):

        data = next(self.handle)
        if data:
            return data

        raise StopIteration






