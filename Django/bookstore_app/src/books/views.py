from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Book

class BookListView(ListView):
    model = Book
    template_name = 'books/main.html'
    
class BookDetailView(DetailView):                       
    model = Book                                        
    template_name = 'books/detail.html' 