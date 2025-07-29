from django.db import models

# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=225)
    author = models.CharField(max_length=225)
    description = models.TextField()
    year = models.PositiveIntegerField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.title 