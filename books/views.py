from django.shortcuts import render
from rest_framework.decorators import api_view
from .models import Book
from rest_framework.response import Response
from .serializers import BookSerializer
from rest_framework import status
# Create your views here.

@api_view(['GET'])
def get_books(request):
    # Use prefetch_related to optimize the query and avoid N+1 problem
    books = Book.objects.prefetch_related('reviews').all()
    
    # Pass the books to the serializer (which already includes reviews)
    serializer = BookSerializer(books, many=True)
    
    return Response(serializer.data)

@api_view(['POST'])
def post_book(request):
  serializer = BookSerializer(data=request.data)
  if serializer.is_valid():
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)
  return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT','PATCH'])
def update_book(request , pk):
    try:
       book= Book.objects.get(pk=pk)
    except Book.DoesNotExist:
       return Response({'error':'Book Not Found'},status=status.HTTP_404_NOT_FOUND) 
    serializer=BookSerializer(book,data=request.data, partial=True) # partial=True allows PATCH
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_book(request,pk):
   try:
      book = Book.objects.get(pk=pk)
   except Book.DoesNotExist:
      return Response({'error':'Book Not Found'},status=status.HTTP_404_NOT_FOUND)  
   book.delete()
   return Response({'message':'Book Deleted Successfully'},status=status.HTTP_204_NO_CONTENT)
   

