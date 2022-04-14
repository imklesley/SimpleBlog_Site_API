from django.urls import path

from .views import create_post_view, user_posts_view,detail_post_view,delete_post_view,edit_post_view

app_name = 'post'

urlpatterns = [
    path('create/', create_post_view, name='create_post'),
    path('my_posts/', user_posts_view, name='user_posts'),
    path('<str:slug>/', detail_post_view, name='detail_post'),
    path('<str:slug>/delete', delete_post_view, name='delete_post'),
    path('<str:slug>/edit', edit_post_view, name='edit_post'),
]
