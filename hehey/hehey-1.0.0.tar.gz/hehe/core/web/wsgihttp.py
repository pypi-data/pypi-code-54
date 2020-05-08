
from urllib import parse;
import re,sys,cgi
import tempfile
import os,shutil;

"""
 * wsgi http 解析类
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
class WsgiHttpParser(object):

    RAW = "raw"
    FILE = "file"
    FIELD = "field"

    def __init__(self,environ,charset = '',max_file_size = 0):

        self.environ = environ;
        self.charset = charset;

        # 默认100M 100 * 1024 * 1024
        self.max_file_size = max_file_size;
        # body 最大的数值
        self.data_upload_max_memory_size = 1024*1024 *10 ;

        # 计算body 长度
        try:
            self.contentLength = int(self.environ.get('CONTENT_LENGTH', 0))
        except (ValueError):
            self.contentLength = 0

        contentType = self.environ.get("CONTENT_TYPE", "")
        contentTypeItems = contentType.split(';')
        self.contentType = contentTypeItems.pop(0);

        options = {};
        for name_value in contentTypeItems:
            item = name_value.split('=')
            options[item[0].lstrip()] = item[1]

        self.content_type_options = options;

    # 获取编码
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre
    def getCharset(self):

        if hasattr(self,'_charset'):
            return getattr(self,'_charset')

        if self.charset:
            return self.charset;

        charset = self.content_type_options.get('charset','utf-8')
        setattr(self,'_charset',charset)

        return charset;

    # 解析wsgi 请求入口
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre
    def parse(self):

        forms = {};
        files = {}

        # 校验body 的大小
        if self.data_upload_max_memory_size > 0:
            inputSize = sys.getsizeof(self.environ['wsgi.input']);

            if inputSize >  self.data_upload_max_memory_size:
                raise Exception('Request body exceeded settings.DATA_UPLOAD_MAX_MEMORY_SIZE')

        # 读取整个post 内容
        if self.contentType == 'multipart/form-data':
            forms,files = self._parseMultipart();
        elif self.contentType == 'application/x-www-form-urlencoded':
            forms,files = self._parseUrlencoded();
        elif self.contentType == 'application/x-url-encoded':
            forms,files = self._parseUrlencoded();

        return self._formatFormsFields(forms),self._formatFileFields(files)

    # 格式化普通参数
    # <B> 说明： </B>
    # <pre>
    # 一般为get,post 参数
    # </pre
    def _formatFormsFields(self,fields):

        columns = {};

        for (name, value) in fields:
            key = name;
            #columns[key] = value
            self.formatKeyValue(columns,key,value)

        return columns;

    def formatKeyValue(self,columns, name, value):
        # 支持数组
        reg = r'\[(\w+)?\]';
        regedx = re.compile(reg)
        matches = regedx.findall(name);

        if matches:
            firstName = name.split('[')[0]
            firstValue = columns.get(firstName, None)

            keylen = len(matches)
            i = 0;
            if matches[0] == '':
                if firstValue is None:
                    firstValue = [];
                    columns[firstName] = firstValue;

                firstValue.append(value);
            else:
                if firstValue is None:
                    firstValue = {};
                    columns[firstName] = firstValue;

                for key in matches:
                    if key not in firstValue.keys():
                        firstValue[key] = {};

                    i = i + 1;
                    if keylen == i:
                        firstValue[key] = value;
                    else:
                        firstValue = firstValue.get(key)


        else:
            firstName = name;
            columns[firstName] = value

        return;



    # 格式化文件参数
    # <B> 说明： </B>
    # <pre>
    # 一般为get,post 参数
    # </pre
    def _formatFileFields(self,fields):

        columns = {};

        for (name, value) in fields:
            key = name;
            #columns[key] = value;
            self.formatKeyValue(columns, key, value)

        return columns;

    # 解析上传文件
    # <B> 说明： </B>
    # <pre>
    # 解析multipart/form-data post 内容数据
    # </pre
    def _parseMultipart(self):

        forms = []
        files = []

        streamHttpBody = self.environ['wsgi.input'].read(self.contentLength)

        boundary = self.content_type_options['boundary']

        # 验证boundary 合法性
        if not boundary or not cgi.valid_boundary(boundary):
            raise Exception('invalid boundary in multipart: %s' % boundary.decode())

        boundaryLen = len(boundary) + 4;
        streamHttpBody = streamHttpBody[boundaryLen:]

        if isinstance(boundary, str):
            boundary = boundary.encode('ascii')

        # post 分割结束符
        splitBoundary = b'--' + boundary + b'\r\n';
        # 怎么会多出个结束符 boundary+ '--',想不明白,截取结束符
        endboundary = b'--' + boundary + b'--\r\n';
        streamHttpBody = streamHttpBody[0:-len(endboundary)];
        boundaryDataList = streamHttpBody.split(splitBoundary)

        for boundaryDataBuffer in boundaryDataList:
            if boundaryDataBuffer == endboundary:
                continue;

            parsePostItemResult =  self.parsePostItem(boundaryDataBuffer)
            if not parsePostItemResult:
                continue;

            item_type,field_name,meta_data = parsePostItemResult

            if item_type == self.FILE:
                # 上传文件
                files.append((field_name.decode(),meta_data))
            elif item_type == self.FIELD:
                # 普通表单字段
                forms.append((field_name.decode(), meta_data.decode(self.getCharset())))

        return forms,files;


    # 解析每个post 字段字符串
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre
    def parsePostItem(self,post_item):

        boundaryHeaderBuffer,boundaryValueBuffer = post_item.split(b"\r\n\r\n",2)
        # 删除 boundaryValueBuffer 尾部\r\n
        boundaryValueBuffer = boundaryValueBuffer[:-len(b"\r\n")]

        # 判断是否文件
        boundaryHeader = boundaryHeaderBuffer.split(b"\r\n",2)
        regex = re.compile(b'name="(.*?)"; filename="(.*?)"$')
        filematch = regex.findall(boundaryHeader[0]);
        if filematch:
            item_type = self.FILE
            field_name = filematch[0][0];
            # 文件内容未空,则不创建临时文件
            if not boundaryValueBuffer:
                return ;

            # 校验文件最大限制
            fileSize = sys.getsizeof(boundaryValueBuffer);
            if self.max_file_size > 0:
                if fileSize > self.max_file_size:
                    raise Exception('Request file exceeded settings.max_file_size')

            # 写入临时文件
            tempf = self.createTempfile();
            tempf.write(boundaryValueBuffer);
            meta_data = {"name":bytes.decode(filematch[0][1]),'tmp_name':tempf.name,"temp":tempf,'type':None,'size':fileSize}
            content_type, content_type_value = boundaryHeader[1].split(b": ")
            content_type = content_type.lower()
            if content_type == "content-type":
                meta_data['type'] = content_type_value;

            return [item_type, field_name, TempUploadFile(**meta_data)]
        else:
            item_type = self.FIELD
            regex = re.compile(b'name="(.*?)"$')
            fieldmatch = regex.findall(boundaryHeaderBuffer);
            # 普通字段
            if fieldmatch:
                field_name = fieldmatch[0]
                meta_data = boundaryValueBuffer;
                return item_type,field_name,meta_data

        return ;

    # 创建新的临时文件
    # <B> 说明： </B>
    # <pre>
    # 用于接收post 过来的文件
    # </pre
    def createTempfile(self):

        fp = tempfile.NamedTemporaryFile('w+b', delete=True)

        return fp;

    # 解析普通post 字段
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre
    def _parseUrlencoded(self):

        forms = {};
        files = {};

        if self.contentLength:
            content = self.environ['wsgi.input'].read(self.contentLength)
            forms,files = self.formatQuery(content,self.charset),{}

        return forms, files;

    # 处理请求表单数据
    # <B> 说明： </B>
    # <pre>
    # 格式name=111&ok=222&name=222
    # </pre
    def formatQuery(self,query_string,encoding):

        query_string = query_string.decode(encoding)
        # 编码
        if isinstance(query_string, bytes):
            try:
                query_string = query_string.decode(encoding)
            except UnicodeDecodeError:
                query_string = query_string.decode('iso-8859-1')

        parse_qsl_kwargs = {
            'keep_blank_values': True,
            'fields_limit': None,
            'encoding': encoding,
        }

        paramsList = self._parse_query_params(query_string,**parse_qsl_kwargs)

        # 继续解析字段名
        params = [];

        for name,value in paramsList:
            params.append((name,value));

        return params


    # 解析参数
    # <B> 说明： </B>
    # <pre>
    # 常用url,form 表单数据解析
    # </pre
    def _parse_query_params(self,query_string, keep_blank_values = False, encoding='utf-8',
                          errors = 'replace', fields_limit = None):

        split_char_match = re.compile('[&;]')

        if fields_limit:
            params = split_char_match.split(query_string, fields_limit)
            if len(params) > fields_limit:
                raise Exception('The number of GET/POST parameters exceeded settings.DATA_UPLOAD_MAX_NUMBER_FIELDS.')
        else:
            params = split_char_match.split(query_string)

        paramsList = []

        for name_value in params:

            if not name_value:
                continue

            nv = name_value.split('=', 1)

            if len(nv) != 2:
                if keep_blank_values:
                    nv.append('')
                else:
                    continue

            if nv[1] or keep_blank_values:
                name = nv[0].replace('+', ' ')
                name = parse.unquote(name, encoding=encoding, errors=errors)
                value = nv[1].replace('+', ' ')
                value = parse.unquote(value, encoding=encoding, errors=errors)
                paramsList.append((name, value))

        return paramsList


"""
 * 文件上传基类
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
class BaseUploadFile:


    def __init__(self,**attrs):

        # 文件名称
        # <B> 说明： </B>
        # <pre>
        # 略
        # </pre>
        self.name = '';

        # 临时文件
        # <B> 说明： </B>
        # <pre>
        # 略
        # </pre>
        self.temp = ''

        # 临时文件路径
        # <B> 说明： </B>
        # <pre>
        # 略
        # </pre>
        self.tmp_name = ''

        # 文件类型
        # <B> 说明： </B>
        # <pre>
        # 略
        # </pre>
        self.type = None

        # 文件大小
        # <B> 说明： </B>
        # <pre>
        # 略
        # </pre>
        self.size = 0

        for attr in attrs:
            setattr(self, attr, attrs[attr])

    def todic(self):

        return {
            'name': self.name,
            'temp':self.temp,
            'type': self.type,
            'size': self.size,
            'tmp_name':self.tmp_name
        };

    def getName(self):

        return self.name;


    def getType(self):

        return self.type

    # 文件大小
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    def size(self):

        pass

    # 以块的方式读取文件
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    def chunks(self,chunk_size):

        while True:
            data = self.read(chunk_size)
            if not data:
                break
            yield data

    # 读取文件
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    def read(self):

        return ;

    # 移动文件
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    def move(self,newFilepath):

        pass


"""
 * 临时文件上传
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
class TempUploadFile(BaseUploadFile):

    def __init__(self,**attrs):

        super().__init__(**attrs);

    def size(self):

        size = os.path.getsize(self.temp)

        return size;



    def read(self):

        self.temp.seek(0);

        return self.temp.read()

    def chunks(self, chunk_size):

        self.temp.seek(0);
        while True:
            data = self.temp.read(chunk_size)
            if not data:
                break
            yield data

    def move(self,newFilepath):

        self.temp.seek(0);
        fpath, fname = os.path.split(newFilepath)
        if not os.path.exists(fpath):
            os.makedirs(fpath)

        self.temp.seek(0);
        with open(newFilepath, 'wb') as f:
            f.write(self.temp.read())

        return True;


class MemoryUploadedFile(BaseUploadFile):

    def __init__(self,**attrs):

        super().__init__(**attrs);

    def size(self):

        size = os.path.getsize(self.temp)

        return size;

    def read(self):

        data = '';

        with open(self.temp, 'r') as f:
            data = f.read()

        return data

    def chunks(self, chunk_size = 1024):

        with open(self.temp, 'r') as f:
            while True:
                data = f.read(chunk_size)
                if not data:
                    break
                yield data

    def move(self,newFilepath):

        fpath, fname = os.path.split(newFilepath)
        if not os.path.exists(fpath):
            os.makedirs(fpath)

        shutil.move(self.temp, newFilepath)

        return True;