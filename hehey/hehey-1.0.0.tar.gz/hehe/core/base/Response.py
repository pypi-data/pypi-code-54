# -*- coding: utf-8 -*-

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

class Response:


    def __init__(self):

        # 响应原始内容
        # <B> 说明： </B>
        # <pre>
        # 略
        # </pre>
        self.content = "";

    # 设置内容
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre
    def setContent(self,content = ''):

        self.content = content;

    def getContent(self):

        if self.content is None:
            self.content = ''

        return self.content;

    def send(self):

        return ;




