from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.index, name='index'),
    path("posts/<str:slug>/", views.post_detail, name="post_detail"),
    path("posts/", views.PostListView.as_view(), name='post_list'),
    path("posts/<str:slug>/comment", views.post_comment, name='post_comment'),
    path("search/", views.post_search, name='post_search'),
    # path("posts/",views.post_list,name='post_list'),
    # path("posts/<str:slug>/", views.PostDetailView.as_view(), name="post_detail"),

]
