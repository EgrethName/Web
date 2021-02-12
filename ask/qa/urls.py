from django.urls import re_path, path
from . import views


urlpatterns = [
    path('', views.main, name='main'),
    re_path('popular/', views.popular, name='popular'),
    re_path(r'question/(?P<number>\d+)/', views.one_question, name='one_question'),
    path('ask/', views.ask, name='ask'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.site_login, name='site_login'),
]
