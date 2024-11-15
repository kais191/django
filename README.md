https://chat-dgqh.onrender.com


#-  save method in Profile model
This custom save method in the Profile model ensures that profile images are resized to a maximum of 300x300 pixels when saved.
Non-trivial aspects:
This method uses the PIL library (Image) to handle image resizing.

def save(self, *args, **kwargs):
    super().save(*args, **kwargs)

    img = Image.open(self.image.path)

    if img.height > 300 or img.width > 300:
        output_size = (300, 300)
        img.thumbnail(output_size)
        img.save(self.image.path)


#- form_valid in PostCreateView and PostUpdateView
This method sets the author of a post to the currently logged-in user before saving it.
Non-trivial aspects:
By overriding form_valid, this function enforces that the author of a post is the currently logged-in user, preventing users from setting any other author.

def form_valid(self, form):
    form.instance.author = self.request.user
    return super().form_valid(form)

#-  test_func in PostUpdateView and PostDeleteView 
This method is used to control access to update and delete actions for a post.
Non-trivial aspects:
test_func provides a powerful way to enforce ownership permissions on views.

def test_func(self):
    post = self.get_object()
    if self.request.user == post.author:
        return True
    return False


#- chat_response
This function simulates a simple chatbot by providing a random response to user messages.
Non-trivial aspects:
Uses JsonResponse to return data in JSON format, which is often used in APIs and dynamic web applications.

def chat_response(request):
    if request.method == "POST":
        user_message = request.POST.get("message")
        bot_response = random.choice(AUTO_RESPONSES)
        return JsonResponse({"user_message": user_message, "bot_response": bot_response})



#- toggle_favorite
//This function allows users to add or remove a post from their favorites.
 Non-trivial aspects:
 get_object_or_404 automatically raises a 404 error if the Post is not found.

def toggle_favorite(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user in post.favorites.all():
        post.favorites.remove(request.user)
    else:
        post.favorites.add(request.user)
    return redirect('blog-home')

#- about_view
//This function renders an "About" page that displays the latest posts, announcements, and events.
Non-trivial aspects:
Using order_by('-date_posted')[:5] to limit the query results to the latest 5 posts is efficient and avoids fetching unnecessary data.

def about_view(request):
    latest_posts = Post.objects.order_by('-date_posted')[:5]
    announcements = Announcement.objects.all()[:5]
    calendar_events = Event.objects.all()[:5]
    
   context = {
        'latest_posts': latest_posts,
        'announcements': announcements,
        'calendar_events': calendar_events,
    }
    
    return render(request, 'blog/about.html', context),
    

    
