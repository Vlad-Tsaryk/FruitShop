from django.shortcuts import render

from bank.models import Bank
from fruits.models import Fruit


# Create your views here.
def index(request):
    fruits = Fruit.objects.all()
    bank = Bank.objects.first()
    return render(request, 'main_page.html', context={'fruits': fruits, 'bank': bank})

# def
