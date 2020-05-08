from .utils import CommonUtil

"""
 * 解析配置文件类
 *<B>说明：</B>
 *<pre>
 *  略
 *</pre>
"""
class Config():

    def __init__(self,files = [],basePath = ''):

        self.files = files

        self.basePath = basePath

        # 配置扩展名对应的处理方法
        # <B> 说明： </B>
        # <pre>
        # 略
        # </pre>
        self.extHandler = {
            'py': self._pyHandler,
            'ini': self._iniHandler,
            'yaml': self._yamlHandler,
            'json': self._jsonHandler,
        }

        return ;

    def addHandler(self,ext,pyHandler):

        self.extHandler[ext] = pyHandler

        return self;

    @classmethod
    def get(cls,files,basePath = ''):

        conf = cls(files,basePath)

        return conf.parse();

    def parse(self):

        confs = {}
        for filepath in self.files:
            if self.basePath:
                filepath = self.basePath + '/' + filepath
            conf = self._getConf(filepath)
            if conf:
                confs.update(conf);

        return confs

    def _getConf(self,filepath):

        ext = CommonUtil.getFileExt(filepath)
        handler = self.extHandler.get(ext, None)

        if handler is None:
            parserClazz = self._buildParserClazz(ext)
            parserMeta= CommonUtil.getClassMeta(parserClazz)
            parser = parserMeta();
            return parser.parse(filepath)
        else:

            # 判断是方法还是类
            if isinstance(handler,str):
                if handler.find('.') == -1:
                    parserClazz = self._buildParserClazz(handler)
                    parserMeta = CommonUtil.getClassMeta(parserClazz)
                    parser = parserMeta();
                else:
                    parser = CommonUtil.getClassMeta(handler)

                return parser.parse(filepath)
            else:
                return handler(filepath);

    def _buildParserClazz(self,parser):

        parserName = CommonUtil.ucfirst(parser)
        parserClazzName = parserName + 'Parser'
        parserClazz = "{0}.parser.{1}.{2}".format(__package__, parserClazzName, parserClazzName)

        return parserClazz


    def _pyHandler(self,filepath):

        with open(filepath, 'r') as f:
            packageFileCode = f.read()

        params = {
            "config": {}
        };

        exec(packageFileCode, params)
        return params['config']

    def _iniHandler(self,filepath):

        import configparser;
        cf = configparser.ConfigParser()
        cf.read(filepath, encoding='utf8')

        items = dict(cf._sections)
        messages = {}

        for key in items:
            messages[key] = dict(items[key])

        # 读取其他配置文件
        return messages;

    def _yamlHandler(self,filepath):

        import yaml
        messages = {}
        with open(filepath, 'r') as f:
            messages = yaml.full_load(f.read())

        return messages

    def _jsonHandler(self,filepath):

        import json
        messages = {}
        with open(filepath, 'r') as f:
            messages = json.load(f)

        return messages

