from django.urls import path
from .views import (
    HomeView, AdminDashboardView, ManageUsersView,
    PromoteUserView, DeactivateUserView, ManageReviewsView
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
]
