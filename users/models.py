from django.db import models
from django.contrib.auth.models import User
from PIL import Image  # To handle image resizing (optional)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        """
        Override the save method to ensure a default image path and resize profile images, if necessary.
        """
        # Set a default image path if none is provided
        if not self.image:
            self.image = 'profile_pics/default.jpg'  # Adjust this path as needed

        super().save(*args, **kwargs)  # Save the profile instance first
        
        # Optional resizing of the image
        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)
