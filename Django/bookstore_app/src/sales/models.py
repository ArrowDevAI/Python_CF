from django.db import models
from books.models import Book

# Create your models here.
class Sale(models.Model):
    book = models.ForeignKey(Book, on_delete = models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.FloatField(help_text = 'in USD $')
    date_created = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return str(f"Book: {self.book} Qty Sold: {self.quantity} Price: {self.price} Sold on: {date_created}")