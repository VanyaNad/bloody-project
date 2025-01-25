from django.contrib import admin
from .models import Article, Topic, Comment, Subscription

admin.site.register(Article)
admin.site.register(Topic)
admin.site.register(Comment)
admin.site.register(Subscription)
