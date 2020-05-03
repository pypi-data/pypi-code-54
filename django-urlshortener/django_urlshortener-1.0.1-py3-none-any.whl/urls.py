from django.conf.urls import re_path
from urlshortener import views


app_name = "urlshortener"


urlpatterns = [
    re_path(r'^$', views.HomepageView.as_view(), name="homepage"),
    re_path(r'^(?P<slug>[\w-]+)/$', views.URLShortenerDetailView.as_view(), name="url_shortener_detail"),
]
