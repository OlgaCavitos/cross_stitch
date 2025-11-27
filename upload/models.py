from django.db import models

# Create your models here.

from django.db import models

class UploadedImage(models.Model):
    image = models.ImageField(upload_to='images/')  # папка media/images
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image {self.id}"



from django.contrib.auth.models import User

class Calculation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="calculations")
    number = models.IntegerField()
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Розрахунок {self.number} ({self.user.username})"
