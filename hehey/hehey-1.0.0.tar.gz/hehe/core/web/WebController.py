# -*- coding: utf-8 -*-
"""
 * 控制器基类
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

from hehe.core.base.BaseController import BaseController
from .WebResponse import WebResponse
from hehe import he

class WebController(BaseController):


    def actions(self):

        return ;

    def redirect(self,url,statusCode = 302):

        return he.app.hresponse.redirect(url,statusCode);

    def beforeAction(self):

        return True;

    def validate(self,dataList = None,rules = [] ,scenes = {},clearErrors = True):

        validationResult = he.app.hvalidation.validate(dataList,rules,scenes,clearErrors);
        setattr(self,'_validationResult',validationResult)

        return validationResult.getResult();

    def getValidError(self):

        if hasattr(self,'_validationResult'):
            validationResult = getattr(self,'_validationResult')
            return validationResult.getFirstError()
        else:
            return ''

    def sendFile(self,filePath, attachmentName = None, **options):

        return he.app.hresponse.sendFile(filePath, attachmentName, **options);

    def assign(self,name,value = None):

        return he.app.hview.assign(name,value);

    def fetch(self,template,data = {}):

        return he.app.hview.fetch(template,data);

    def post(self,name = None,defaultValue = None):

        return he.app.hrequest.getPost(name,defaultValue);

    def query(self,name = None,defaultValue = None):

        return he.app.hrequest.getQuery(name,defaultValue);

    def request(self,name = None,defaultValue = None):

        return he.app.hrequest.getRequest(name,defaultValue);

    def isAjax(self):

        return he.app.hrequest.isAjax();

    def isGet(self):

        return he.app.hrequest.isGet();

    def isPost(self):

        return he.app.hrequest.isPost();

    def ajaxError(self,code,message,data = {}):

        return self.sendAjaxJson(self.buildDataFormat(code,message,data));

    def ajaxSuccess(self,message,data = {},code = 0):

        return self.sendAjaxJson(self.buildDataFormat(code,message,data));

    def buildDataFormat(self,code,message = '',data = {}):

        return {
            'code':code,
            'message':message,
            'data':data
        };

    def sendAjaxJson(self,data = {}):

        he.app.hresponse.formatter = WebResponse.FORMAT_JSON
        he.app.hresponse.setContent(data);

        return he.app.hresponse;

