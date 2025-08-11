from django.conf.global_settings import AUTH_USER_MODEL
from django.db.models import (
    CASCADE,
    BooleanField,
    CharField,
    DateTimeField,
    EmailField,
    ForeignKey,
    Index,
    Manager,
    Model,
    SlugField,
    TextChoices,
    TextField,
)
from django.urls import reverse
from django.utils import timezone


class PublishedManager(Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)


class Post(Model):
    class Status(TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    title = CharField(max_length=250)
    slug = SlugField(max_length=250, unique_for_date='publish')
    author = ForeignKey(AUTH_USER_MODEL, on_delete=CASCADE, related_name='blog_posts')
    body = TextField()
    publish = DateTimeField(default=timezone.now)
    created = DateTimeField(auto_now_add=True)
    updated = DateTimeField(auto_now=True)
    status = CharField(max_length=2, choices=Status, default=Status.DRAFT)
    objects = Manager()
    published = PublishedManager()

    class Meta:
        ordering = ['-publish']
        indexes = [Index(fields=['-publish'])]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.publish.year, self.publish.month, self.publish.day, self.slug])


class Comment(Model):
    post = ForeignKey(Post, on_delete=CASCADE, related_name='comments')
    name = CharField(max_length=80)
    email = EmailField()
    body = TextField()
    created = DateTimeField(auto_now_add=True)
    updated = DateTimeField(auto_now=True)
    active = BooleanField(default=True)


    class Meta:
        ordering = ['created']
        indexes = [Index(fields=['created'])]

    def __str__(self):
        return f'Comment by {self.name} on {self.post}'