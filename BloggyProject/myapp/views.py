# Create your views here.
from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    FormView,
    TemplateView,
)
from .models import Article, Topic, Comment, Subscription
from .forms import ArticleForm, CommentForm, TopicForm


class RegisterView(View):
    def get(self, request):
        form = UserCreationForm()
        return render(request, 'blog/register.html', {'form': form})

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        return render(request, 'blog/register.html', {'form': form})


class ArticleListView(LoginRequiredMixin, ListView):
    model = Article
    template_name = 'blog/index.html'
    context_object_name = 'articles'
    ordering = ['-created_at']


class MyFeedView(LoginRequiredMixin, ListView):
    model = Article
    template_name = 'blog/my_feed.html'
    context_object_name = 'articles'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            subscribed_topics = Subscription.objects.filter(user=self.request.user).values_list('topic', flat=True)
            return Article.objects.filter(topics__in=subscribed_topics).distinct()
        else:
            return Article.objects.none()


class ArticleDetailView(LoginRequiredMixin, DetailView):
    model = Article
    template_name = 'blog/article_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['top_level_comments'] = Comment.objects.filter(article=self.object, parent=None)
        return context


class CreateArticleView(LoginRequiredMixin, CreateView):
    model = Article
    form_class = ArticleForm
    template_name = 'blog/create_article.html'
    success_url = "/"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class UpdateArticleView(LoginRequiredMixin, UpdateView):
    model = Article
    form_class = ArticleForm
    template_name = 'blog/update_article.html'
    success_url = reverse_lazy('index')

    def get_success_url(self):
        return reverse_lazy('article_detail', kwargs={'pk': self.object.pk})

    def get_object(self, queryset=None):
        return get_object_or_404(Article, id=self.kwargs['article_id'])


class DeleteArticleView(LoginRequiredMixin, DeleteView):
    model = Article
    template_name = 'blog/delete_article.html'
    success_url = reverse_lazy('index')



class TopicListView(ListView):
    model = Topic
    template_name = 'blog/topic_list.html'
    context_object_name = 'topics'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            user_subscriptions = Subscription.objects.filter(user=self.request.user).values_list('topic_id', flat=True)
            topics = context['topics']
            for topic in topics:
                topic.is_subscribed = topic.id in user_subscriptions
        return context


class TopicArticlesView(LoginRequiredMixin, ListView):
    template_name = 'blog/topic_articles.html'
    context_object_name = 'articles'

    def get_queryset(self):
        topic = get_object_or_404(Topic, id=self.kwargs['topic_id'])
        return topic.articles.all()


class ArticlesByDateView(LoginRequiredMixin, ListView):
    template_name = 'blog/articles_by_date.html'
    context_object_name = 'articles'

    def get_queryset(self):
        year = self.kwargs['year']
        month = self.kwargs['month']
        return Article.objects.filter(created_at__year=year, created_at__month=month)


class ProfileView(TemplateView):
    template_name = 'blog/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # Subscribed topics
        context['subscribed_topics'] = Subscription.objects.filter(user=user).select_related('topic')

        # User's articles
        context['user_articles'] = Article.objects.filter(author=user)

        # User's top-level comments
        context['user_comments'] = Comment.objects.filter(author=user, parent=None).select_related('article')
        return context


class SubscribeToTopicView(LoginRequiredMixin, View):
    def post(self, request, topic_id, *args, **kwargs):
        topic = get_object_or_404(Topic, id=topic_id)
        if request.user.is_authenticated:
            Subscription.objects.get_or_create(user=request.user, topic=topic)
        return redirect('topic_list')


class UnsubscribeFromTopicView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        topic = get_object_or_404(Topic, id=kwargs['topic_id'])
        Subscription.objects.filter(user=request.user, topic=topic).delete()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


class DeleteProfileView(LoginRequiredMixin, View):
    template_name = 'blog/delete_profile.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        user = request.user
        logout(request)
        user.delete()
        return redirect('login')


class AddCommentView(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        article = get_object_or_404(Article, pk=pk)
        parent_comment = None

        # Check if replying to a comment
        if 'parent_id' in request.POST:
            parent_id = request.POST.get('parent_id')
            parent_comment = get_object_or_404(Comment, id=parent_id)

        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.article = article
            comment.parent = parent_comment
            comment.save()
            return redirect('article_detail', pk=article.pk)
        return render(request, 'blog/article_detail.html', {'form': form, 'article': article})


@method_decorator(staff_member_required, name='dispatch')
class CreateTopicView(View):
    def get(self, request, *args, **kwargs):
        form = TopicForm()
        return render(request, 'blog/create_topic.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = TopicForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('topic_list')
        return render(request, 'blog/create_topic.html', {'form': form})
