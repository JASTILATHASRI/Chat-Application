from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('', views.home, name='home'),
    path('chat/<int:user_id>/', views.chat_view, name='chat'),
    path('logout/', LogoutView.as_view(), name='logout'),
]