from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Recipe
from django.contrib.auth.mixins import LoginRequiredMixin

def Main(request):
    return render(request, 'recipes/home.html')


class RecipeListView(LoginRequiredMixin,ListView):
    model = Recipe
    template_name = "recipes/list.html"

class RecipeDetailView(LoginRequiredMixin,DetailView):                       
    model = Recipe                                        
    template_name = 'recipes/detail.html' 