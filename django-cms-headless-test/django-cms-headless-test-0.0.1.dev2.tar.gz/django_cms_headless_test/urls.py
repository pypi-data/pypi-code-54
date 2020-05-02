from django.conf.urls import url

from .views import (AllPagesView, PageDetails)

urlpatterns = [
    url(r'^pages/$', AllPagesView.as_view(), name='cms_page_detail_home'),
    url(r'pages/path/(?P<path>.*)/$', PageDetails.as_view(), name='page'),
]

app_name = 'headless'