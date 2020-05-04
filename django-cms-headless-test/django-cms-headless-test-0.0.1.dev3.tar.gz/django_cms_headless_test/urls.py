from django.conf.urls import url

from .views import (AllPagesView, PageDetails)

urlpatterns = [
    url(r'^pages/$', AllPagesView.as_view(), name='all_pages_view'),
    url(r'pages/path/(?P<path>.*)/$', PageDetails.as_view(), name='single_page_view'),
]

app_name = 'headless'