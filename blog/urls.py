from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from .views import (
    PostlistView, 
    PostDetailView, 
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    UserPostListView
)

urlpatterns = [
    path('post/<int:post_id>/favorite/', views.toggle_favorite, name='toggle-favorite'),
    path('about/', views.about_view, name='about'),  # This is the about view; remove duplicate below
    path('chat_response/', views.chat_response, name='chat_response'),
    path('', PostlistView.as_view(), name='blog-home'),
    path('user/<str:username>/', UserPostListView.as_view(), name='user-posts'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('delete_message/', views.delete_message, name='delete_message')
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
