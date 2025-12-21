from django.urls import path
from .views import (
    HomeView, AdminDashboardView, ManageUsersView,
    PromoteUserView, DeactivateUserView, ManageReviewsView,
    DeleteReviewView, AddDoctorView, AddPatientView, AddRoomView
)

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('admin-dashboard/', AdminDashboardView.as_view(), name='admin-dashboard'),
    
    # User Management
    path('admin/users/', ManageUsersView.as_view(), name='manage-users'),
    path('admin/users/<int:user_id>/promote/', PromoteUserView.as_view(), name='promote-user'),
    path('admin/users/<int:user_id>/deactivate/', DeactivateUserView.as_view(), name='deactivate-user'),
    
    # Review Management
    path('admin/reviews/', ManageReviewsView.as_view(), name='manage-reviews'),
    path('admin/reviews/<int:pk>/delete/', DeleteReviewView.as_view(), name='delete-review'),
    
    # Custom Admin Add Forms
    path('admin/doctors/add/', AddDoctorView.as_view(), name='add-doctor'),
    path('admin/patients/add/', AddPatientView.as_view(), name='add-patient'),
    path('admin/rooms/add/', AddRoomView.as_view(), name='add-room'),
]
