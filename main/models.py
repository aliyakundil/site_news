from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils import timezone
from taggit.managers import TaggableManager
from django.contrib.auth.models import User


class IpModel(models.Model):
    ip = models.CharField(max_length=100)

    def __str__(self):
        return self.ip

class Post(models.Model):
    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        ordering = ['-created_date']

    # author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Автор')
    title = models.CharField(max_length=222, verbose_name='Заголовок')
    text = models.TextField(blank=True, verbose_name='Текст')
    created_date = models.DateTimeField(default=timezone.now, verbose_name='Дата создания')
    published_date = models.DateTimeField(blank=True, null=True, verbose_name='Дата публикации')
    image = models.ImageField(upload_to='images/news/%Y/%m/%d', blank=True,
                              verbose_name='Фото')
    id_published = models.BooleanField(default=True, verbose_name='Опубликовано')
    category_id = models.ForeignKey('Category', on_delete=models.CASCADE, verbose_name='Категория')
    tags = TaggableManager()
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    views = models.ManyToManyField(IpModel, related_name="post_views", blank=True)
    likes = models.ManyToManyField(IpModel, related_name="post_likes", blank=True)


    def total_views(self):
        return self.views.count()

    def total_likes(self):
        return self.likes.count()
    # objects = models.Manager()  # The default manager
    # published = PublishedManager()  # Custom manager



    def publish(self):
        self.published_date = timezone.now()
        self.save()


    def __str__(self):
        return self.title

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
