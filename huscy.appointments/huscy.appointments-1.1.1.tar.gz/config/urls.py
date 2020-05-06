from django.contrib import admin
from django.urls import include
from django.urls import path

from huscy.appointments.feed import AppointmentFeed
from huscy.appointments.feed import get_feed_url


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/', include('huscy.appointments.urls')),
    path('feed/<str:token>', AppointmentFeed(), name='feed'),
    path('feedurl/', get_feed_url, name='feed-url'),

]
