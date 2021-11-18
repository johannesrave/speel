from django.urls import path, include
from player import views
# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('player/', views.Index.as_view(), name='player'),
]
