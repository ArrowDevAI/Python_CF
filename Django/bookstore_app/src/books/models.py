from django.db import models
from django.shortcuts import reverse

genre_choices= (
        ('classic','Classic'),
        ('romantic','Romantic'),
        ('comic','Comic'),
        ('fantasy','Fantasy'),
        ('horror','Horror'),
        ('educational','Educational'),
        ('sci-fi', 'Sci-Fi')
        )

book_type_choices = (
        ('hardcover','Hard cover'),
        ('ebook','E-Book'),
        ('audiob','Audiobook')
        )

class Book(models.Model):
    name = models.CharField(max_length = 120, verbose_name = 'name')
    genre = genre = models.CharField(max_length=12,choices=genre_choices,default='classic')
    book_type = book_type = models.CharField(max_length=12,choices=book_type_choices,default='hardcopy')
    price = models.FloatField(help_text = 'in USD $')
    author_name = models.CharField(max_length=120)
    pic = models.ImageField(upload_to='books', default = 'no_picture.jpg')
    
    def __str__(self):
        return str(f"Name: {self.name} Author: {self.author_name}")
    
    def get_absolute_url(self):
       return reverse('books:detail', kwargs={'pk': self.pk})
