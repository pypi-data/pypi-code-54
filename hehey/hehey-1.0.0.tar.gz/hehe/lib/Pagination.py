# -*- coding: utf-8 -*-
import importlib,inspect
from hehe import he
from math import ceil

"""
 * 分页类
 *<B>说明：</B>
 *<pre>
 *  略
 *</pre>
 *<B>示例：</B>
 *<pre>
 *  略
 *</pre>
"""
class Pagination:



    def __init__(self,pageSize = None,params = None):

        # 读取条数
        # <B> 说明： </B>
        # <pre>
        # 略
        # </pre
        self.limit = 10

        # 总条数
        # <B> 说明： </B>
        # <pre>
        # 略
        # </pre
        self.totalCount = 0;

        # 设置页码限制
        # <B> 说明： </B>
        # <pre>
        # 略
        # </pre
        self.pageSize = pageSize;

        # 默认页码大小
        # <B> 说明： </B>
        # <pre>
        # 略
        # </pre
        self.defaultPageSize = 10;

        # 每页大小限制
        # <B> 说明： </B>
        # <pre>
        # 略
        # </pre
        self.pageSizeLimit = [1,50];

        # 页码参数名称
        # <B> 说明： </B>
        # <pre>
        # 略
        # </pre
        self.pageParam = 'page'

        # 每页大小参数名称
        # <B> 说明： </B>
        # <pre>
        # 略
        # </pre
        self.pageSizeParam = 'per-page'

        # 数据
        # <B> 说明： </B>
        # <pre>
        # 略
        # </pre
        self.data = None;

        # 请求参数
        # <B> 说明： </B>
        # <pre>
        # 略
        # </pre
        self.params = params;


        self._init = False;


        self._pageSize = None;

        self._page = None;


        self.maxButtonCount = 10;


    def getLimit(self):

        return self.getPageSize();


    # 获取分页偏移量
    # <B> 说明： </B>
    # <pre>
    # 数据读取的起始记录标识
    # </pre
    def getOffset(self):

        pageSize = self.getPageSize();

        if pageSize <= 1:
            return 0;
        else:
            return (self.getPage() - 1) * pageSize

        return 0;

    def setTotalCount(self,totalCount):

        self.totalCount = totalCount

        return ;

    def setData(self,data):

        self.data = data

        return ;

    def getData(self):

        return self.data


    def getPage(self,recalculate = False):

        if self._page is None or recalculate:
            _page = int(self._getQueryParam(self.pageParam,1))
            self.setPage(_page)

        return self._page;


    def setPage(self,page):

        if page is None:
            self._page = None;
        else:
            _page = int(page)
            if _page < 0:
                _page = 1;

            self._page = _page

        return ;


    def getPageSize(self):

        if self._pageSize is None:
            psize = self.pageSize
            if psize is None:
                psize = self._getQueryParam(self.pageSizeParam, self.defaultPageSize)

            if not self.pageSizeLimit:
                self.setPageSize(psize)
            else:
                self.setPageSize(psize,True)


        return self._pageSize;


    def setPageSize(self,pageSize,validatePageSize = False):

        if pageSize is None:
            self._pageSize = None;
        else:
            _pageSize = int(pageSize)
            if validatePageSize and isinstance(self.pageSizeLimit,list) and len(self.pageSizeLimit) == 2:
                if  _pageSize < self.pageSizeLimit[0]:
                    _pageSize = self.pageSizeLimit[0]
                elif _pageSize > self.pageSizeLimit[1]:
                    _pageSize = self.pageSizeLimit[1]

            self._pageSize = _pageSize

        return ;



    def _getQueryParam(self,name,defaultValue):

        if self.params is None:
            self.params = he.app.hrequest.getQuery();

        return self.params.get(name,defaultValue)


    def getPageCount(self):

        pageSize = self.getPageSize();

        if self.totalCount < 0:
            totalCount = 0;
        else:
            totalCount = int(self.totalCount)


        return ceil(totalCount/pageSize);


    # 分页基本参数
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre
    def buildShowParams(self):

        params = {};
        currentPage = self.getPage();
        pageCount = self.getPageCount();

        if currentPage <= 1:
            # 首页
            params['first'] = ''
            # 上一页
            params['prev'] = ''
        else:
            # 首页
            params['first'] = he.app.toUrl('', {self.pageParam: 1})
            # 上一页
            params['prev'] = he.app.toUrl('', {self.pageParam: currentPage - 1})


        if currentPage >= pageCount:
            # 下一页
            params['next'] = ''
            # 尾页
            params['last'] = ''
        else:
            # 下一页
            params['next'] = he.app.toUrl('', {self.pageParam: currentPage + 1})
            # 尾页
            params['last'] = he.app.toUrl('', {self.pageParam: pageCount})


        # 每页大小
        params['page_size'] = self.getPageSize()
        # 总页数
        params['page_total'] = pageCount

        params['total_count'] = self.totalCount

        # 当前页面
        params['page_cur'] = currentPage

        return params;

    def _getPageNumberRange(self):

        currentPage = self.getPage();
        pageCount = self.getPageCount();
        beginPage = max(1,currentPage - int(self.maxButtonCount / 2))
        endPage = beginPage + self.maxButtonCount

        if endPage >= pageCount:
            endPage = pageCount;
            beginPage = max(1, endPage - self.maxButtonCount + 1);


        return [beginPage,endPage]


    def buildNumber(self):

        beginPage, endPage = self._getPageNumberRange()

        numbers = [];

        for num in range(beginPage,endPage + 1):
            numbers.append((num,he.app.toUrl('', {self.pageParam: num})))


        return numbers;




