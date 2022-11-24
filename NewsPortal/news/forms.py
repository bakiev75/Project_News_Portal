from django import forms
from .models import Post

class PostForm(forms.ModelForm):
   class Meta:
       model = Post
       fields = [
           'author',
           'article_or_new',
           'title',
           'text_body',
           'date_time_post',
           'rating_article_or_new',
           'category',
       ]