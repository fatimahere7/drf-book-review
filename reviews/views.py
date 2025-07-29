from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes,authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Review, Book
from .serializers import ReviewSerializer
from rest_framework.authentication import TokenAuthentication,SessionAuthentication,BasicAuthentication

@api_view(['GET'])
def get_reviews(request, book_id):
    try:
        book = Book.objects.get(pk=book_id)
    except Book.DoesNotExist:
        return Response({'error': 'Book not found'}, status=404)

    reviews = Review.objects.filter(book=book)
    serializer = ReviewSerializer(reviews, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication,TokenAuthentication])
@permission_classes([IsAuthenticated])
def add_review(request, book_id):
    
    try:
        book = Book.objects.get(pk=book_id)
    except Book.DoesNotExist:
        return Response({'error': 'Book not found'}, status=404)

    # prevent duplicate review by same user
    if Review.objects.filter(book=book, user=request.user).exists():
        return Response({'error': 'You have already reviewed this book.'}, status=400)

    serializer = ReviewSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user, book=book)
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

