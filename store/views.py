#/home/siisi/e-commerce/store/views.py

from django.shortcuts import render
from datetime import datetime, timezone


def home(request):
    date = datetime.now(timezone.utc).strftime("%a %d %B %Y")
    
    context = {
        'date' : date,
    }
    return render(request, 'index.html', context)
