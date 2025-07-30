from django.contrib import admin
from django.urls import path, include
from books import views as book_views
from reviews import views as review_views
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('accounts.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('books/', book_views.get_books,name='get_books'),
    path('books/create/', book_views.post_book, name='post_book'),
    path('books/<int:pk>/update/', book_views.update_book, name='update_book'),
    path('books/<int:pk>/delete/', book_views.delete_book, name='delete_book'),
    path('books/<int:book_id>/reviews/', review_views.get_reviews, name='get_reviews'),
    path('books/<int:book_id>/reviews/add/', review_views.add_review, name='add_review'),
]