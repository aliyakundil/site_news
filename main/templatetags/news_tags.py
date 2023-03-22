from main.models import Category, Post
from django import template
from django.db.models import Count, F

register = template.Library()


@register.simple_tag()
def get_categories():
    return Post.objects.all()

@register.inclusion_tag('main/show_category.html')
def last_post(count=3):
    return {'last_post':Post.objects.order_by('-id')[:count]}

@register.simple_tag()
def get_categories2(count=3):
    return Post.objects.order_by('-id')[:count]
