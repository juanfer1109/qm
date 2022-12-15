from . import views
from django.urls import path

urlpatterns = [
    path('post', views.PostList.as_view(), name='post_list'),
    path('<slug:slug>/', views.PostDetail.as_view(), name='post_detail'),
]