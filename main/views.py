from .forms import PostForm, UserRegisterForm, UserLoginForm
from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth import login, logout
from datetime import datetime, timedelta
from rest_framework import viewsets
from .serializers import *
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from taggit.models import Tag
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views.generic import ListView,DetailView
from .models import *
from django.http import HttpResponseRedirect


class TagMixin(object):
    def get_context_data(self, **kwargs):
        context = super(TagMixin, self).get_context_data(**kwargs)
        context['tags'] = Tag.objects.all()
        return context


class PostIndexView(TagMixin, ListView):
    model = Post
    template_name = 'main/index.html'
    queryset = Post.objects.all()
    context_object_name = 'posts'


class TagIndexView(TagMixin, ListView):
    model = Post
    template_name = 'main/index.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Post.objects.filter(tags__slug=self.kwargs.get('tag_slug'))


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


class PostDetailView(DetailView):
    model = Post
    context_object_name = 'blog'
    template_name = 'blog-detail.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)

        # adding like count
        like_status = False
        ip = get_client_ip(request)
        if self.object.likes.filter(id=IpModel.objects.get(ip=ip).id).exists():
            like_status = True
        else:
            like_status = False
        context['like_status'] = like_status

        return self.render_to_response(context)


def postLike(request, pk):
    post_id = request.POST.get('post-id')
    post = Post.objects.get(pk=post_id)
    ip = get_client_ip(request)
    if not IpModel.objects.filter(ip=ip).exists():
        IpModel.objects.create(ip=ip)
    if post.likes.filter(id=IpModel.objects.get(ip=ip).id).exists():
        post.likes.remove(IpModel.objects.get(ip=ip))
    else:
        post.likes.add(IpModel.objects.get(ip=ip))
    return HttpResponseRedirect(reverse('post_detail', args=[post_id]))


def index(request):
    post = Post.objects.all()
    category2 = Category.objects.all
    common_tags = Post.tags.most_common()[:4]
    return render(request, 'main/index.html', {'post':post, 'category2':category2, 'common_tags':common_tags})

def all_news(request):
    post = Post.objects.all()
    category2 = Category.objects.all
    return render(request, 'main/all_news.html', {'post':post, 'category2':category2})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'main/post_detail.html', {'post': post})

def post_new(request):
    form = PostForm(request.POST)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.published_date = timezone.now()
        try:
            post.image = request.FILES['image']
        except:
            post.image = post.image
        post.save()
        return redirect('/', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'main/post_new.html', {'form': form})

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post.title = request.POST['title']
            post.text = request.POST['text']
            post.author = request.user
            post.published_date = timezone.now()
            try:
                post.image = request.FILES['image']
            except:
                post.image = post.image

            post.save()
            return redirect('/', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'main/post_edit.html', {'form': form})

def post_delete(request, pk):
    news = Post.objects.get(pk=pk)
    news.delete()
    return redirect('/')

def filter(request, pk):
    post = Post.objects.all()
    if pk == 1:
        now = datetime.now() - timedelta(minutes=60*24*7)
        post = post.filter(created_date__gte=now)
    elif pk == 2:
        now = datetime.now() - timedelta(days=30)
        post = post.filter(created_date__lte=now)
    elif pk == 3:
        post = post

    return render(request, 'main/filter.html', {'post':post})



# def likes(self, request, pk, *args, **kwargs):
#     post = Likes.objects.get(pk=pk)
#
#     is_dislike = False
#
#     for dislike in post.dislikes.all():
#         if dislike == request.user:
#             is_dislike = True
#             break
#
#     if is_dislike:
#         post.dislikes.remove(request.user)
#
#     is_like = False
#
#     for like in post.likes.all():
#         if like == request.user:
#             is_like = True
#             break
#
#     if not is_like:
#         post.likes.add(request.user)
#
#     if is_like:
#         post.likes.remove(request.user)
#
#     return render(reverse('likes', args=[str(pk)]))

def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'login user')
            return redirect('/')
        else:
            messages.error(request, 'Error login')
    else:
        form = UserLoginForm()
    return render(request, 'register/login.html', {'form':form})

def user_logout(request):
    logout(request)
    return redirect('index')

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Register Success')
            return redirect('/')
        else:
            messages.error(request, 'Register Error')
    else:
        form = UserRegisterForm()
    return render(request, 'register/register.html', {'form':form})

def show_category(request, pk):
    post = Post.objects.filter(pk=pk)
    all_category = Category.objects.all()
    return render(request, 'main/show_category.html', {
        'all_category' : all_category,
        'post':post
    })

# #  Поиск
# Post.objects.annotate(
#     search = SearchVector('title', 'text')
# ).filter(seacrh='django')

# #  Поиск
# def post_seacrh(request):
#     form = SearchForm()
#     if 'query' in request.GET:
#         if form.is_valid():
#             cd = form.cleaned_data
#             results = SeacrhQuerySet().models(Post).filter(content=cd['query']).load_all()
#             total_result = results.count()
#     return render(request, 'main/search.html',
#                   { 'form': form,
#                     'cd': cd,
#                     'results':results,
#                     'total_result': total_result})



class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = ['text']
    search_fields = ['author', 'title']
    ordering_fields = ['author', 'text']
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthenticated]

    def perform_create(self, serializer):
        serializer.validated_data['user'] = self.request.user
        serializer.save()

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


def post_detail_view(request, pk):
    handle_page = get_object_or_404(Post, id=pk)
    total_comments = handle_page.comments_blog.all().filter(reply_comment=None).order_by('-id')
    total_comments2 = handle_page.comments_blog.all().order_by('-id')
    total_likes = handle_page.total_likes_post()
    total_saves = handle_page.total_saves_posts()

    context = {}

    context['post'] = handle_page
    return render(request, 'main/post_detail.html', context)

import sys
print(sys.getrecursionlimit())


# def tags(request, tag_slug):
#     tag = get_object_or_404(Tag, slug=tag_slug)
#     posts = Post.objects.filter(tags__in=[tag]).order_by('-posted')
#
#     context = {
#         'tag': tag,
#         'posts': posts,
#     }
#
#
#     return render(request, 'tags.html', context)
#
# def detail(request, slug):
#     post = get_object_or_404(Post, slug=slug)
#     return render(request, 'main/detail.html', {'post': post})




# def post_list(request, tag_slug=None):
#     object_list = Post.published.all()
#     tag = None
#
#     if tag_slug:
#         tag = get_object_or_404(Tag, slug=tag_slug)
#         object_list = object_list.filter(tags__in=[tag])
#
#     paginator = Paginator(object_list, 3) # 3 posts in each page
#     page = request.GET.get('page')
#     try:
#         posts = paginator.page(page)
#     except PageNotAnInteger:
#         # If page is not an integer deliver the first page
#         posts = paginator.page(1)
#     except EmptyPage:
#         # If page is out of range deliver last page of results
#         posts = paginator.page(paginator.num_pages)
#     return render(request, 'main/list.html', {'page': page,
#                                                    'posts': posts,
#                                                    'tag': tag})


