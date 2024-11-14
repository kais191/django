from django.urls import path
from . import views
from .views import (
    PostlistView, 
    PostDetailView, 
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    UserPostListView #Imported the PostDeleteView class from views.py
)
from .import views

urlpatterns = [

    path('post/<int:post_id>/favorite/', views.toggle_favorite, name='toggle-favorite'),
    path('about/', views.about_view, name='about'),
    path('chat_response/', views.chat_response, name='chat_response'),
    path('', PostlistView.as_view(), name='blog-home'),
    path('user/<str:username>/', UserPostListView.as_view(), name='user-posts'),
    path('post/<int:pk>', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'), # Added in new url pattern
    path('about/',views.about, name='blog-about'),
    path('delete_message/', views.delete_message, name='delete_message')
    
]

