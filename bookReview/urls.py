from django.contrib import admin
from django.urls import path, include
from books import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('accounts.urls')),
    path('book/', views.get_books,name='get_books'),
    path('books/create/', views.post_book, name='post_book'),
    path('books/<int:pk>/update/', views.update_book, name='update_book'),
    path('books/<int:pk>/delete/', views.delete_book, name='delete_book'),
]