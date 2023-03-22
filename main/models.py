import uuid

from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db.models import Sum
from django.utils.text import slugify


class LikeDislikeManager(models.Manager):
    use_for_related_fields = True

    def likes(self):
        # We take the queryset with records greater than 0
        return self.get_queryset().filter(vote__gt=0)

    def dislikes(self):
        # We take the queryset with records less than 0
        return self.get_queryset().filter(vote__lt=0)

    def sum_rating(self):
        # We take the total rating
        return self.get_queryset().aggregate(Sum('vote')).get('vote__sum') or 0


class LikeDislike(models.Model):
    LIKE = 1
    DISLIKE = -1

    VOTES = (
        (DISLIKE, 'Dislike'),
        (LIKE, 'Like')
    )

    vote = models.SmallIntegerField(choices=VOTES)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    objects = LikeDislikeManager()


from django.db import models
from django.contrib.contenttypes.fields import GenericRelation


class Article(models.Model):
    votes = GenericRelation(LikeDislike, related_query_name='articles')
    def articles(self):
        return self.get_queryset().filter(content_type__model='article').order_by('-articles__pub_date')

class Comment(models.Model):
    votes = GenericRelation(LikeDislike, related_query_name='comments')
    def comments(self):
        return self.get_queryset().filter(content_type__model='comment').order_by('-comments__pub_date')

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset()\
    .filter(status='published')

class Tag(models.Model):
    title = models.CharField(max_length=100, verbose_name='Tag')
    slug = models.SlugField(null=False, unique=True, default=True)

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

    def get_absolute_url(self):
        return reverse('tags', args=[self.slug])

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug - slugify(self.slug)
        return super().save(*args, **kwargs)

class Post(models.Model):
    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        ordering = ['-created_date']

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Автор')
    title = models.CharField(max_length=222, verbose_name='Заголовок')
    text = models.TextField(blank=True, verbose_name='Текст')
    created_date = models.DateTimeField(default=timezone.now, verbose_name='Дата создания')
    published_date = models.DateTimeField(blank=True, null=True, verbose_name='Дата публикации')
    image = models.ImageField(upload_to='images/news/%Y/%m/%d', blank=True,
                              verbose_name='Фото')
    id_published = models.BooleanField(default=True, verbose_name='Опубликовано')
    likes = models.ManyToManyField(User, blank=True, related_name='Лайки')
    category_id = models.ForeignKey('Category', on_delete=models.CASCADE, verbose_name='Категория')
    tags = TaggableManager()

    objects = models.Manager()  # The default manager
    published = PublishedManager()  # Custom manager

    def publish(self):
        self.published_date = timezone.now()
        self.save()


    def __str__(self):
        return self.title

    # def get_absolute_url(self):
    #     return reverse('blog:post_detail',
    #                        args=[self.slug])


    def get_absolute_url(self):
        return reverse('new_detail', kwargs={'pk': self.pk})


class Category(models.Model):
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['title']  # автосортировка

    title = models.CharField(max_length=222, db_index=True, verbose_name='Наименование категорий')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('category', kwargs={'category_id': self.pk})
