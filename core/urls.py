from django.urls import path

from core import views

urlpatterns = [
    path("history/", views.ScrapeRecordListView.as_view(), name="scrape-history"),
    path("", views.NewsItemListView.as_view(), name="news-link-list"),
]
