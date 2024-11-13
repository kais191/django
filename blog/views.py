from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render
from django.http import JsonResponse
import json
import random
from .models import Post, Announcement, Event 
from .models import Post
from django.shortcuts import get_object_or_404, redirect






def toggle_favorite(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user in post.favorites.all():
        post.favorites.remove(request.user)
    else:
        post.favorites.add(request.user)
    return redirect('blog-home')  # Or wherever you want to redirect





def about_view(request):
    latest_posts = Post.objects.order_by('-date_posted')[:5]  # Get the latest 5 posts
    announcements = Announcement.objects.all()[:5]  # Get the latest 5 announcements
    calendar_events = Event.objects.all()[:5]  # Get the latest 5 events
    
    context = {
        'latest_posts': latest_posts,
        'announcements': announcements,
        'calendar_events': calendar_events,
    }
    
    return render(request, 'blog/about.html', context)


def delete_message(request):
    if request.method == "POST":
        # Retrieve and process the message ID or other data sent from the frontend
        data = json.loads(request.body)
        message_id = data.get('messageId')
        
        # Perform deletion or logging actions here, if needed
        # For example, deleting from a database if you store messages

        return JsonResponse({"status": "success", "message": "Message deleted."})
    return JsonResponse({"status": "error", "message": "Invalid request."})

# Example auto-responses
AUTO_RESPONSES = [
    "Hello! How can I help you?",
    "I’m here to assist you with any questions.",
    "Feel free to ask anything!",
    "I'm just an auto-responder, but I'll try my best!",
]

def about_view(request):
    return render(request, 'blog/about.html')

def chat_response(request):
    if request.method == "POST":
        user_message = request.POST.get("message")
        bot_response = random.choice(AUTO_RESPONSES)
        return JsonResponse({"user_message": user_message, "bot_response": bot_response})






from django.views.generic import (
    ListView, 
    DetailView, 
    CreateView,
    UpdateView,
    DeleteView # New import added here
)
from django.http import HttpResponse
from .models import Post

# Create your views here.x
def home(request):
    context = {
       'posts': Post.objects.all()
    }
    return render(request, 'blog/home.html', context)

class PostlistView(ListView):
    model = Post
    template_name = 'blog/home.html' #<app>/<model>_<viewtype>.html
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
        if self.request.user == post.author:
            return True
        return False
    
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView): # New class PostDeleteView created here
    model = Post
    
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = "/" # Here we are redirecting the user back to the homepage after deleting a Post successfully
    
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
    
    

class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html' # ‹app>/<model >_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 5
