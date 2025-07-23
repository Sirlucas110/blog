from django.conf.global_settings import AUTH_USER_MODEL
from django.db.models import (
    CASCADE,
    CharField,
    DateTimeField,
    ForeignKey,
    Index,
    Manager,
    Model,
    SlugField,
    TextChoices,
    TextField,
)
from django.utils import timezone


class PublishedManager(Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)


class Post(Model):
    class Status(TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    title = CharField(max_length=250)
    slug = SlugField(max_length=250)
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
