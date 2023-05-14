from django.shortcuts import render

from fruits.models import Fruit


# Create your views here.
def index(request):
    fruits = Fruit.objects.all()
    return render(request, 'main_page.html', context={'fruits': fruits})
