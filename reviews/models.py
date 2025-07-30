from django.db import models
from django.conf import settings  # Import settings to access AUTH_USER_MODEL
from accounts.models import CustomUser
from books.models import Book

class Review(models.Model):
    book = models.ForeignKey(Book, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    review_number = models.PositiveIntegerField(default=1)
    class Meta:
        ordering = ['created_at']
        unique_together = ['user', 'book', 'review_number']
    
    def __str__(self):
        return f"Review {self.review_number} by {self.user.username} for {self.book.title}"