# -*- coding: utf-8 -*-

from hehe import he

from htemplate.view import reg_temp_filter

# 生成url地址
@reg_temp_filter('U')
def url_filter(self,uri,vars = {},**options):

    return he.app.toUrl(uri,vars,**options)


# 生成资源地址
@reg_temp_filter('res')
def res_filter(self,filepath):

    return he.app.home.buildResUrl(filepath)


@reg_temp_filter('L')
def lang_filter(self,name,params = {},app = '',packageName = None,lang = None):

    return he.lang(name,params,app,packageName,lang)