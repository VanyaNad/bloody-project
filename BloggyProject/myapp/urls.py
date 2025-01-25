from django.contrib.auth.views import PasswordChangeDoneView
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (
    ArticleListView,
    MyFeedView,
    ArticleDetailView,
    AddCommentView,
    UpdateArticleView,
    DeleteArticleView,
    CreateArticleView,
    TopicListView,
    TopicArticlesView,
    SubscribeToTopicView,
    UnsubscribeFromTopicView,
    ProfileView,
    DeleteProfileView,
    RegisterView,
    ArticlesByDateView,
    CreateTopicView,
    DeleteTopicView,

)

urlpatterns = [
    path('', ArticleListView.as_view(), name='index'),
    path('my-feed/', MyFeedView.as_view(), name='my_feed'),
    path('<int:pk>/', ArticleDetailView.as_view(), name='article_detail'),
    path('<int:pk>/comment/', AddCommentView.as_view(), name='add_comment'),
    path('<int:article_id>/update/', UpdateArticleView.as_view(), name='update_article'),
    path('<int:pk>/delete/', DeleteArticleView.as_view(), name='delete_article'),
    path('create/', CreateArticleView.as_view(), name='create_article'),
    path('topics/', TopicListView.as_view(), name='topic_list'),
    path('topics/<int:topic_id>/', TopicArticlesView.as_view(), name='topic_articles'),
    path('topics/<int:topic_id>/subscribe/', SubscribeToTopicView.as_view(), name='subscribe_to_topic'),
    path('topics/<int:topic_id>/unsubscribe/', UnsubscribeFromTopicView.as_view(), name='unsubscribe_from_topic'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/delete/', DeleteProfileView.as_view(), name='delete_profile'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='blog/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('set-password/', auth_views.PasswordChangeView.as_view(template_name='blog/set_password.html'), name='set_password'),
    path('<int:year>/<int:month>/', ArticlesByDateView.as_view(), name='articles_by_date'),
    path('topics/create/', CreateTopicView.as_view(), name='create_topic'),
    path('topics/<int:pk>/delete/', DeleteTopicView.as_view(), name='delete_topic'),
    path('set-password/done/', PasswordChangeDoneView.as_view(template_name='blog/password_change_done.html'), name='password_change_done'),
]
