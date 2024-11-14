from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import JsonResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
import json
import random

from .models import Post, Announcement, Event

# Automatic responses for chat bot
AUTO_RESPONSES = [
    "Hello! How can I help you?",
    "I’m here to assist you with any questions.",
    "Feel free to ask anything!",
    "I'm just an auto-responder, but I'll try my best!",
]

def home(request):
    context = {
       'posts': Post.objects.all()
    }
    return render(request, 'blog/home.html', context)

class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted'] 
    paginate_by = 5

class PostDetailView(DetailView):
    model = Post  

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']
     
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']
     
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
    
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = "/"
    
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 5  

@login_required
def toggle_favorite(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user in post.favorites.all():
        post.favorites.remove(request.user)
    else:
        post.favorites.add(request.user)
    return redirect('blog-home')

def about_view(request):
    latest_posts = Post.objects.order_by('-date_posted')[:5]
    announcements = Announcement.objects.all()[:5]
    calendar_events = Event.objects.all()[:5]
    
    context = {
        'latest_posts': latest_posts,
        'announcements': announcements,
        'calendar_events': calendar_events,
    }
    
    return render(request, 'blog/about.html', context)

def delete_message(request):
    if request.method == "POST":
        data = json.loads(request.body)
        message_id = data.get('messageId')
        return JsonResponse({"status": "success", "message": "Message deleted."})
    return JsonResponse({"status": "error", "message": "Invalid request."})

def chat_response(request):
    if request.method == "POST":
        user_message = request.POST.get("message")
        bot_response = random.choice(AUTO_RESPONSES)
        return JsonResponse({"user_message": user_message, "bot_response": bot_response})
