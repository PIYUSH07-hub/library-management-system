from django.urls import path
from .views import issue_book_view, return_book_view
from . import views
from .views import import_books

urlpatterns = [
    path('issue/', issue_book_view, name='issue-book'),
    path('return/', return_book_view, name='return-book'),
    path('search/', views.search_books, name='search_books'),
    path('import/', import_books, name='import_books'),
]
