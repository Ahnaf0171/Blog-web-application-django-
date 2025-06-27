from django import forms
from .models import Post, Comment

class Post_form(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'picture', 'category_id', 'tag']

class comment_form(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

