# -*- coding: utf-8 -*-

"""
 * 应用组件帮助类
 *<B>说明：</B>
 *<pre>
 *  无任何功能作用,只用用于ide代码提示
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


class Component(object):

    @property
    def hevent(self):
        """
        :rtype :hehe.core.hevent.event.EventManager
        """
        pass

    @property
    def hrouter(self):
        """
        :rtype :hehe.core.hrouter.route.RouterManager
        """
        pass

    @property
    def hconfig(self):
        """
        :rtype :hehe.core.hconfig.config.Config
        """
        pass

    @property
    def hrequest(self):
        """
        :rtype :hehe.core.base.Request.Request|hehe.core.web.WebRequest.WebRequest
        """
        pass

    @property
    def hresponse(self):
        """
        :rtype :hehe.core.base.Response.Response|hehe.core.web.WebResponse.WebResponse
        """
        pass

    @property
    def hvalidation(self):
        """
        :rtype :hehe.core.hvalidation.ValidationIde.ValidationIde
        """
        pass

    @property
    def hsession(self):
        """
        :rtype :hehe.core.hsession.base.WebSession.WebSession
        """
        pass

    @property
    def hdbsession(self):
        """
        :rtype :hdb.Dbsession.Dbsession
        """
        pass

    @property
    def hevent(self):
        """
        :rtype :hehe.core.hevent.event.EventManager
        """
        pass

    @property
    def hview(self):
        """
        :rtype :hehe.core.hview.view.View
        """
        pass

    @property
    def hlog(self):
        """
        :rtype :hehe.core.hlogger.logger.LogManager
        """
        pass

    @property
    def hcache(self):
        """
        :rtype :hcache.cache.CacheManager
        """
        pass

    @property
    def hclient(self):
        """
        :rtype :hclient.client.Client
        """
        pass

    @property
    def hupload(self):
        """
        :rtype :hupload.upload.UploadManager
        """
        pass

    @property
    def hqueue(self):
        """
        :rtype :hqueue.queue.QueueManager
        """
        pass

    @property
    def hi18n(self):
        """
        :rtype :hehe.core.hi18n.I18n.I18n
        """
        pass

    @property
    def hid(self):
        """
        :rtype :hid.IdManagerIde.IdManagerIde
        """
        pass

    @property
    def hscheduler(self):
        """
        :rtype :hehe.core.hscheduler.SchedulerManagerIde.SchedulerManagerIde
        """
        pass

    @property
    def hmiddleware(self):
        """
        :rtype :hehe.core.hmiddleware.MiddlewareManager.MiddlewareManager
        """
        pass





