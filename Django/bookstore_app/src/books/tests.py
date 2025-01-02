from django.test import TestCase
from .models import Book

class BookModelTest(TestCase):
    
    def setUpTestData():
        Book.objects.create(
            name = 'Enders Game', 
            author_name = 'Orson Scott Card', 
            book_type = 'hardcover', 
            genre = 'sci-fi', 
            price = 13.67
            )
    def test_book_name(self):
        book = Book.objects.get(id =1)
        field_label = book._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')
    
    def test_author_name_max_length(self):
        book = Book.objects.get(id=1)
        max_length = book._meta.get_field('author_name').max_length
        self.assertEqual( max_length, 120 )

