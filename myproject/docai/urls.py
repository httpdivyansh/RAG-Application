
from django.urls import path
from . import views  # Relative import

urlpatterns = [
    # path('', views.index, name='index'),
    path('', views.log_in, name='log_in'),
    path('home/', views.home, name='home'),
    path('register/', views.register, name='register'),
]