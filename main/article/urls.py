from django.contrib import admin
from django.urls import path
from .views import ArticleView,ArticleById

urlpatterns = [
    path('articles/', ArticleView.as_view()),
    path('articles/<int:id>/',ArticleById.as_view())
]
