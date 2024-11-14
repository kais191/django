from django.db import models
from django.contrib.auth.models import User
from PIL import Image  # To handle image resizing (optional)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='profile_pics/default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        # Use the default image if no image is provided
        if not self.image:
            self.image = 'profile_pics/default.jpg'
        super().save(*args, **kwargs)
        
        # Resize image if needed
        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)
