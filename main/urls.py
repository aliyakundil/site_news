from django.urls import path, re_path
from .views import *
from rest_framework import routers

from django.contrib.auth.decorators import login_required

from . import views
# from .models import LikeDislike

routers = routers.SimpleRouter()

routers.register(r'news', PostViewSet)
routers.register(r'category', CategoryViewSet)

# from . import views
# from .models import LikeDislike, Article

# app_name = 'ajax'

# app_name="like_button"

urlpatterns = [

    # path('', views.blog_index, name = 'blog_index'),


    path('', index, name='index'),
    path('all_news/', all_news, name='all_news'),
    path('post_edit/<int:pk>/edit/', post_edit, name='post_edit'),
    path('post_delete/<int:pk>/', post_delete, name='post_delete'),
    # path('<int:pk>/like/', AddLike.as_view(), name='like'),
    path('post/<int:pk>/', post_detail, name='post_detail'),
    # path('post/<int:pk>/', post_list, name='post_list'),
    # path('post/<slug:post_slug>/', post_detail, name='post_detail'),

    # path('<slug>/$', views.DetailView.as_view(), name='detail'),

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


    # path('like/<int:pk>', postLike, name='blog_like'),

    # re_path(r'^$',like_button, name='like'),
    #
    # re_path(r'^article/(?P<pk>\d+)/like/$',
    #     login_required(views.VotesView.as_view(model=Article, vote_type=LikeDislike.LIKE)),
    #     name='article_like'),
    # re_path(r'^article/(?P<pk>\d+)/dislike/$',
    #     login_required(views.VotesView.as_view(model=Article, vote_type=LikeDislike.DISLIKE)),
    #     name='article_dislike'),

    # path('liked/', like_unlike_post, name='like-post-view'),
    # path("like_post", views.like_post, name="like"),

    # path("like/<int:pk>/", liked_video, name="like-video"),
    # path("dislike/<int:pk>/", dislike_video, name="dislike-video"),
    # path('like/<int:pk>', views.postLike, name='blog_like'),

    ]

urlpatterns += routers.urls