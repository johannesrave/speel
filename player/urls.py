from django.urls import path, include
from player import views
# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', views.Index.as_view, name='player'),
]
