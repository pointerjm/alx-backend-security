from django.contrib import admin
from django.urls import path
from ip_tracking import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('anon/', views.anonymous_view),
    path('auth/', views.authenticated_view),
]
