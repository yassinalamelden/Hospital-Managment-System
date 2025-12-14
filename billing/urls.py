from django.urls import path
from .views import BillListView, BillCreateView, BillDetailView

urlpatterns = [
    path('bills/', BillListView.as_view(), name='bill-list'),
    path('bills/add/', BillCreateView.as_view(), name='bill-create'),
    path('bills/<int:pk>/', BillDetailView.as_view(), name='bill-detail'),
]
