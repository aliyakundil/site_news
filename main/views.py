from .forms import PostForm, UserRegisterForm, UserLoginForm
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
from django.views.generic import ListView, DetailView
from .models import *
import json
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.http import HttpResponse


def blog_index(request):
    posts = Post.objects.all()
    return render(request, 'main/blog_index.html', {'posts': posts})


def blog_detail(request, slug):
    post = Post.objects.get(slug=slug)

    msg = False

    if request.user.is_authenticated:
        user = request.user

        if post.likes.filter(id=user.id).exists():
            msg = True


    return render(request, 'main/blog_detail.html',
                  {'post': post, 'msg': msg})


def like_post(request):
    data = json.loads(request.body)
    id = data["id"]
    post = Post.objects.get(id=id)
    checker = None

    if request.user.is_authenticated:

        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
            checker = 0


        else:
            post.likes.add(request.user)
            checker = 1

    likes = post.likes.count()

    info = {
        "check": checker,
        "num_of_likes": likes
    }

    return JsonResponse(info, safe=False)

def index(request):
    post = Post.objects.all()
    category2 = Category.objects.all
    common_tags = Post.tags.most_common()[:4]

    # paginator = Paginator(post_list, 3)
    #
    # # page_number is initialized to `1` see main.js
    # page_number = request.GET.get('page')
    #
    # # we are applying page number which defaults to `1`
    # page_obj = paginator.get_page(page_number)
    #
    # if page_number:
    #
    #     if int(page_number) <= paginator.num_pages:
    #         obj_list = paginator.get_page(page_number)
    #
    #         obj_list = obj_list.object_list.values()
    #
    #         return JsonResponse(list(obj_list), status=200, safe=False)
    return render(request, 'main/index.html', {'post':post, 'category2':category2, 'common_tags':common_tags})

# def like(request, pk):
#     post = Post.objects.get(pk=pk)
#     ip = get_client_ip(request)
#     if request.user.is_authenticated:
#         user = request.user
#
#         if post.likes.filter(id=user.id).exists():
#             msg = True
#
#     if IpLikes.objects.filter(ip=ip).exists():
#         post.views.add(IpModel.objects.get(ip=ip))
#     else:
#         IpModel.objects.create(ip=ip)
#         post.views.add(IpModel.objects.get(ip=ip))
#     return render(request, 'main/index.html', {'post': post, 'msg': msg})

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

# def postLike(request, pk):
#     post_id = request.POST.get('blog-id')
#     post = Post.objects.get(pk=post_id)
#     ip = get_client_ip(request)
#     if not IpLikes.objects.filter(ip=ip).exists():
#         IpLikes.objects.create(ip=ip)
#     if post.likes.filter(id=IpLikes.objects.get(ip=ip).id).exists():
#         post.likes.remove(IpLikes.objects.get(ip=ip))
#     else:
#         post.likes.add(IpLikes.objects.get(ip=ip))
#     return HttpResponseRedirect(reverse('/', args=[post_id]))

def all_news(request):
    post = Post.objects.all()
    category2 = Category.objects.all
    return render(request, 'main/all_news.html', {'post':post, 'category2':category2})

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR') # В REMOTE_ADDR значение айпи пользователя
    return ip



def post_detail(request, pk):
    # post = get_object_or_404(Post, pk=pk)
    post = Post.objects.get(pk=pk)
    ip = get_client_ip(request)
    msg = False
    if request.user.is_authenticated:
        user = request.user

        if post.likes.filter(id=user.id).exists():
            msg = True


    if IpModel.objects.filter(ip=ip).exists():
        post.views.add(IpModel.objects.get(ip=ip))
    else:
        IpModel.objects.create(ip=ip)
        post.views.add(IpModel.objects.get(ip=ip))
    return render(request, 'main/post_detail.html', {'post': post, 'msg':msg})

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


# def post_detail_view(request, pk):
#     handle_page = get_object_or_404(Post, id=pk)
#
#     context = {}
#
#     context['post'] = handle_page
#     return render(request, 'main/post_detail.html', context)


def detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    msg = False
    if request.user.is_authenticated:
        user = request.user

        if post.likes.filter(id=user.id).exists():
            msg = True

    return render(request, 'main/detail.html', {'post': post, 'msg':msg})




def post_list(request, tag_slug=None):
    object_list = Post.published.all()
    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])

    paginator = Paginator(object_list, 3)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request, 'main/list.html', {'page': page,
                                                   'posts': posts,
                                                   'tag': tag})


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


# def get_client_ip(request):
#     x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
#     if x_forwarded_for:
#         ip = x_forwarded_for.split(',')[0]
#     else:
#         ip = request.META.get('REMOTE_ADDR')
#     return ip


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


def blog_detail(request, slug):
    post = Post.objects.get(slug=slug)
    msg = False

    if request.user.is_authenticated:
        user = request.user

        if post.likes.filter(id=user.id).exists():
            msg = True

    return render(request, 'blog_detail.html',
                  {'post': post, 'msg': msg})


def like_post(request):
    data = json.loads(request.body)
    id = data["id"]
    post = Post.objects.get(id=id)
    checker = None

    if request.user.is_authenticated:

        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
            checker = 0


        else:
            post.likes.add(request.user)
            checker = 1

    likes = post.likes.count()

    info = {
        "check": checker,
        "num_of_likes": likes
    }

    return JsonResponse(info, safe=False)