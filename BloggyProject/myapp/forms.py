from django import forms
from .models import Article, Comment, Topic


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content', 'topics']
        widgets = {
            'topics': forms.CheckboxSelectMultiple(),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']


class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['title']