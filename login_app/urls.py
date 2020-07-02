from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('create_user', views.create_user),
    path('success', views.success),
    path('login', views.login),
    path('wall', views.wall),
    path('logout', views.logout),
    path('post', views.post),
    path('delete_post/<int:post_id>', views.delete_post),
    path('comment', views.comment),
    path('delete_comment/<int:comment_id>', views.delete_comment),
]
