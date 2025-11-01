from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('librarian/', views.librarian_dashboard, name='librarian_dashboard'),
    path('my-books/', views.patron_dashboard, name='patron_dashboard'),
]