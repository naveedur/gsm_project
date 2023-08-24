from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views


from.views import *
from.import views

urlpatterns = [
    path('postComment', views.postComment, name="postComment"),
    path('', bloghome, name='blogs'),
    path('article/<slug:mTitle>/<slug:cTitle>/',articles, name="article"),
    path('model/<slug>',models, name='models'),
    path('recent_articles/', solution_articles, name='post'),
    path('solutions/<slug:Title>/',article_solution, name="article-solution"),
    path('article/<slug:postSlug>/', articlepage, name='postpage'),
    path('popular_articles/',popular_artiles, name='popular_articles'),
]

    