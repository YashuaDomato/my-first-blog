from django.urls import path
from .views import BlogView, CommentView, ObtainAuthToken
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('post/', BlogView.post_list_create_view, name='post-list'),
    path('post/<int:pk>', BlogView.post_retrieve_update_destroy_view, name='post-detail'),
    path('post/<int:pk>/comment', CommentView.post_comment_list_create_view, name='post-comment-list'),
    path('comment/', CommentView.comment_list_create_view, name='comment-list'),
    path('comment/<int:pk>', CommentView.comment_retrieve_update_destroy_view, name='comment-detail'),
    path('auth/login', ObtainAuthToken.login),
    path('auth/logout', ObtainAuthToken.logout),
]