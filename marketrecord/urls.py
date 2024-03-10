# urls.py
from django.urls import path
from .views import *


urlpatterns = [

    path('location-create/', LocationCreate.as_view(), name='location-create'),
    path('location-list/', LocationList.as_view(), name='location-list'),
    path('market-create/', MarketCreate.as_view(), name='market-create'),
    path('market-list/', MarketList.as_view(), name='market-list'),
    path('report-create/', ReportCreate.as_view(), name='report-create'),
]