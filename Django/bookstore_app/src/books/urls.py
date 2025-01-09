from django.urls import path
from .views import BookListView
from .views import BookDetailView

app_name = 'books'

urlpatterns = [
    path('list/', BookListView.as_view(), name='list'),
    path('detail/<pk>/', BookDetailView.as_view(), name='detail')
]