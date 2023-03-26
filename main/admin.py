from django.contrib import admin
from .models import *

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_on', 'updated', 'slug')
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(Post)
admin.site.register(Category)
# admin.site.register(LikeButton)
