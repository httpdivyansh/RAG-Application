
from django.urls import path
from . import views  # Relative import

urlpatterns = [
    path('', views.home, name='home'),
]