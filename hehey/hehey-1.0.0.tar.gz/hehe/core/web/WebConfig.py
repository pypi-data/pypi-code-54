# -*- coding: utf-8 -*-
from ..base.Config import Config
from .WebApplication import WebApplication
class WebConfig(Config):


    # 启动应用服务
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    startup = 'wsgiref';

    appClass = WebApplication;






