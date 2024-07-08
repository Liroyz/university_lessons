
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView
from django.contrib.auth import views as auth_views
# from lessons_tracker.tracker.views import ProfileView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('tracker.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', RedirectView.as_view(url='/accounts/login/', permanent=True)),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', include('tracker.urls'))


]
