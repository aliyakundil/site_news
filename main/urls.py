from django.urls import path, re_path
from .views import *
from rest_framework import routers

from django.contrib.auth.decorators import login_required

from . import views
# from .models import LikeDislike

routers = routers.SimpleRouter()

routers.register(r'news', PostViewSet)
routers.register(r'category', CategoryViewSet)

urlpatterns = [
    path('', index, name='index'),
    path('all_news/', all_news, name='all_news'),
    path('post_edit/<int:pk>/edit/', post_edit, name='post_edit'),
    path('post_delete/<int:pk>/', post_delete, name='post_delete'),
    # path('<int:pk>/like/', AddLike.as_view(), name='like'),
    path('post/<int:pk>/', post_detail, name='post_detail'),
    path('post_new/', post_new, name='post_new'),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('filter/<int:pk>/', filter, name='filter'),
    path('show_category/<int:pk>', show_category, name='show_category'),

    re_path(r'^$', views.post_list, name='post_list'),
    re_path(r'^tag/(?P<tag_slug>[-\w]*)/$', views.post_list, name='post_list_by_tag'),
    path('<slug:slug>/',views.detail,name='detail'),


    ]

urlpatterns += routers.urls