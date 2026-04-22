from django.db import models

# Create your models here.
class CustomUser(models.Model):
    google_id=models.CharField(unique=True, max_length=500)
    email=models.EmailField(max_length=254, unique=True)
    timestamp=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.email}-{self.timestamp}"
