from django.urls import path
from .views import BillListView, BillCreateView, BillDetailView, BillStatusUpdateView

urlpatterns = [
    path('bills/', BillListView.as_view(), name='bill-list'),
    path('bills/add/', BillCreateView.as_view(), name='bill-create'),
    path('bills/<int:pk>/', BillDetailView.as_view(), name='bill-detail'),
    path('bills/<int:pk>/status/', BillStatusUpdateView.as_view(), name='bill-status-update'),
]
