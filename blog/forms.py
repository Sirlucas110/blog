from django.forms import Form, CharField, EmailField, Textarea, ModelForm
from blog.models import Comment


class EmailPostForm(Form):
    name = CharField(max_length=25)
    email = EmailField()
    to = EmailField()
    comments = CharField(required=False, widget=Textarea)


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'body']
        