from django.db import models

class Carousel(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='carousel/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
