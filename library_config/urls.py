from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/books/", include("book.urls", namespace="book")),
    path("api/user/", include("user.urls", namespace="user")),
    path("api/borrowings/", include("borrowing.urls", namespace="borrowing")),
]
