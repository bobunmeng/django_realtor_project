from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name = 'index'), # the root path
    path('about', views.about, name = 'about'),
]