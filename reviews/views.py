from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes,authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Review, Book
from .serializers import ReviewSerializer
from rest_framework import status
from rest_framework.authentication import TokenAuthentication,SessionAuthentication,BasicAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication

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
@authentication_classes([SessionAuthentication, BasicAuthentication,JWTAuthentication])
@permission_classes([IsAuthenticated])
def add_review(request, book_id):
    try:
        book = Book.objects.get(pk=book_id)
    except Book.DoesNotExist:
        return Response({'error': 'Book not found'}, status=status.HTTP_404_NOT_FOUND)

    # Get existing reviews count for this user+book combination
    existing_reviews_count = Review.objects.filter(book=book, user=request.user).count()
    
    # Create new review with sequence number
    serializer = ReviewSerializer(data=request.data)
    if serializer.is_valid():
        review = serializer.save(
            user=request.user, 
            book=book,
            review_number=existing_reviews_count + 1  # Add sequence number
        )
        
        response_data = serializer.data
        response_data['review_number'] = review.review_number
        response_data['total_reviews_by_user'] = existing_reviews_count + 1
        
        return Response(response_data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
