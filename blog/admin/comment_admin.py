from blog.models import Comment
from django.contrib.admin import ModelAdmin, register


@register(Comment)
class CommentAdmin(ModelAdmin):
    list_display = ['name', 'email', 'post', 'created', 'active']
    list_filter = ['active', 'created', 'updated']
    search_fields = ['name', 'email', 'body']
