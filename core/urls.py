from django.urls import path

from core import views

urlpatterns = [
    path("", views.NewsItemListView.as_view(), name="news-link-list"),
]
