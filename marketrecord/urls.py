# urls.py
from django.urls import path
from .views import *


urlpatterns = [

    path('location-create/', LocationCreate.as_view(), name='location-create'),
    path('location-list/', LocationList.as_view(), name='location-list'),
    path('market-create/', MarketCreate.as_view(), name='market-create'),
    path('market-list/', MarketList.as_view(), name='market-list'),
    path('report-create/', ReportCreate.as_view(), name='report-create'),
    path('track-report/<int:pk>/', TrackReportView.as_view(), name='track-report'),
    path('report-approve/<int:pk>/', ReportApproveView.as_view(), name='report-approve'),
    path('report-comments/<int:pk>/', ViewReportCommentsView.as_view(), name='report-comments'),
    path('location-report-list/', LocationReportList.as_view(), name='location-report-list'),
    path('user-report-list/', UserReportList.as_view(), name='user-report-list'),
    path('all-report-list/', AllReportList.as_view(), name='all-report-list'),
    path('user-location-market-list/', UserLocationMarketList.as_view(), name='user-location-market-list'),
    
    
]