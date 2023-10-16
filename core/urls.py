from django.urls import path

# from core import views
from core.views import mass_email_view

urlpatterns = [
    path("", mass_email_view, name="index"),
]
