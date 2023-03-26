from django.urls import path, re_path
from .views import *
from rest_framework import routers

from . import views

routers = routers.SimpleRouter()

routers.register(r'news', PostViewSet)
routers.register(r'category', CategoryViewSet)

urlpatterns = [

    path('', index, name='index'),
    path('all_news/', IndexView.as_view(), name='all_news'),
    # path('all_news/', all_news, name='all_news'),
    path('post_edit/<int:pk>/edit/', post_edit, name='post_edit'),
    path('post_delete/<int:pk>/', post_delete, name='post_delete'),
    path('post/<int:pk>/', post_detail, name='post_detail'),
    path('post_new/', post_new, name='post_new'),
    path('register/', register,  name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('filter/<int:pk>/', filter, name='filter'),
    path('show_category/<int:pk>', show_category, name='show_category'),
    re_path(r'^$', views.post_list, name='post_list'),
    re_path(r'^tag/(?P<tag_slug>[-\w]*)/$', views.post_list, name='post_list_by_tag'),
    # path('<slug:slug>/',views.detail,name='detail'),

    path('', PostIndexView.as_view(), name='post-list'),
    path('tags/<slug:tag_slug>/', TagIndexView.as_view(), name='posts_by_tag'),
    path('detail/<int:pk>', PostDetailView.as_view(), name='post_detail'),
    path('article/<slug:slug>', views.post_detail, name='post_detail'),
    path("like_post", views.like_post, name="like")
    ]

urlpatterns += routers.urls