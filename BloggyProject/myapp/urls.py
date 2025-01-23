from django.contrib.auth.views import PasswordChangeDoneView
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.ArticleListView.as_view(), name='index'),
    path('my-feed/', views.MyFeedView.as_view(), name='my_feed'),
    path('<int:pk>/', views.ArticleDetailView.as_view(), name='article_detail'),
    path('<int:pk>/comment/', views.AddCommentView.as_view(), name='add_comment'),
    path('<int:article_id>/update/', views.UpdateArticleView.as_view(), name='update_article'),
    path('<int:pk>/delete/', views.DeleteArticleView.as_view(), name='delete_article'),
    path('create/', views.CreateArticleView.as_view(), name='create_article'),
    path('topics/', views.TopicListView.as_view(), name='topic_list'),
    path('topics/<int:topic_id>/', views.TopicArticlesView.as_view(), name='topic_articles'),
    path('topics/<int:topic_id>/subscribe/', views.SubscribeToTopicView.as_view(), name='subscribe_to_topic'),
    path('topics/<int:topic_id>/unsubscribe/', views.UnsubscribeFromTopicView.as_view(), name='unsubscribe_from_topic'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('profile/delete/', views.DeleteProfileView.as_view(), name='delete_profile'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='blog/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('set-password/', auth_views.PasswordChangeView.as_view(template_name='blog/set_password.html'), name='set_password'),
    path('<int:year>/<int:month>/', views.ArticlesByDateView.as_view(), name='articles_by_date'),
    path('topics/create/', views.CreateTopicView.as_view(), name='create_topic'),
    path('set-password/', views.PasswordChangeView.as_view(template_name='blog/set_password.html'), name='set_password'),
    path('set-password/done/', PasswordChangeDoneView.as_view(template_name='blog/password_change_done.html'), name='password_change_done'),
]
