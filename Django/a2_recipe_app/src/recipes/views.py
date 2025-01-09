from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Recipe

def Main(request):
    return render(request, 'recipes/home.html')

class RecipeListView(ListView):
    model = Recipe
    template_name = "recipes/list.html"

class RecipeDetailView(DetailView):                       
    model = Recipe                                        
    template_name = 'recipes/detail.html' 