# urls.py
from django.urls import path, re_path
from .views import *


urlpatterns = [

    path('component-update/<int:pk>/', ComponentUpdate.as_view(), name='component-update'),
    path('component-create/', ComponentCreate.as_view(), name='component-create'),
    path('component-list/', ComponentList.as_view(), name='component-list'),
    path('location-create/', LocationCreate.as_view(), name='location-create'),
    path('location-list/', LocationList.as_view(), name='location-list'),
    path('market-create/', MarketCreate.as_view(), name='market-create'),
    path('market-update/<int:pk>/', MarketUpdate.as_view(), name='market-update'),
    path('market-delete/<int:pk>/', MarketDelete.as_view(), name='market-delete'),
    path('market-list/', MarketList.as_view(), name='market-list'),
    path('report-create/', ReportCreate.as_view(), name='report-create'),
    path('report-update/<int:pk>/', ReportUpdate.as_view(), name='report-update'),
    path('track-report/<int:pk>/', TrackReportView.as_view(), name='track-report'),
    path('report-approve/<int:pk>/', ReportApproveView.as_view(), name='report-approve'),
    path('report-comments/<int:pk>/', ViewReportCommentsView.as_view(), name='report-comments'),
    path('location-report-list/', UserLocationReportList.as_view(), name='location-report-list'),
    path('user-report-list/', UserReportList.as_view(), name='user-report-list'),
    path('all-report-list/', AllReportList.as_view(), name='all-report-list'),
    path('minister-report-list/', MinisterReportList.as_view(), name='minister-report-list'),
    path('viewers-report-list/', ViewerReportList.as_view(), name='viewers-report-list'),
    path('user-location-market-list/', UserLocationMarketList.as_view(), name='user-location-market-list'),
    re_path(r'^market_occupancy_rate/(?:(?P<year>\d+)/)?$', MarketOccupancyRateView.as_view(), name='market_occupancy_rate'),
    path('season_occupancy_rate/', SeasonOccupancyRateView.as_view(), name='season_occupancy_rate'),
    
    
]