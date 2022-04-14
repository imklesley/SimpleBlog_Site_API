from django.urls import path

from .views import (api_detail_post_view, api_update_post_view, api_delete_post_view, api_create_post_view)

app_name = 'post_api'

urlpatterns = [
    path('create/', api_create_post_view, name='create'),
    path('<slug:slug>', api_detail_post_view, name='detail'),
    path('<slug:slug>/update/', api_update_post_view, name='update'),
    path('<slug:slug>/delete/', api_delete_post_view, name='delete'),
]
