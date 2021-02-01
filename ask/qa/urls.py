from django.urls import re_path, path

from . import views

urlpatterns = [
    path('', views.main, name='main'),
    re_path('popular/', views.popular, name='popular'),
    re_path(r'question/(?P<number>\d+)/', views.one_question, name='one_question')
]
