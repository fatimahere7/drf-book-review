# book/serializers.py
from rest_framework import serializers
from .models import Book
from reviews.serializers import ReviewSerializer

class BookSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)
    
    class Meta:
        model = Book
        fields = ['id', 'title', 'author','description', 'year', 'reviews']