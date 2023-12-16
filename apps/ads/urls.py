from django.urls import path
from .views import (
    AdsListView,
    AdsCreateView, 
    AdsTakeJobView,
    AdsCompleteJobView,
    AdHistoryListView
)

urlpatterns = [
    # URL для показа объявлений
    path('ad_all/', AdsListView.as_view(), name='ads-list'),

    # URL для создания нового объявления
    path('create/', AdsCreateView.as_view(), name='ads-create'),

    # URL для взятия заказа
    path('take/<int:ad_id>/', AdsTakeJobView.as_view(), name='ads-take-job'),

    # URL для завершения выполнения заказа
    path('complete/<int:ad_id>/', AdsCompleteJobView.as_view(), name='ads-complete-job'),

    # URL для показа истории объявлений
    path('history_ads/', AdHistoryListView.as_view(), name='adhistory-list'),
]
