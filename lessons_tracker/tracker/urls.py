from django.urls import path, include
from .views import SignUpView, ProfileView, ScheduleListView, ScheduleDetailView, ScheduleCreateView, ScheduleUpdateView

urlpatterns = [
    path('social-auth/', include('social_django.urls', namespace='social')),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('schedules/', ScheduleListView.as_view(), name='schedule_list'),
    path('schedules/<int:pk>/', ScheduleDetailView.as_view(), name='schedule_detail'),
    path('schedules/create/', ScheduleCreateView.as_view(), name='schedule_create'),
    path('schedules/<int:pk>/edit/', ScheduleUpdateView.as_view(), name='schedule_edit'),

]