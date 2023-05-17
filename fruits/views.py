from django.http import JsonResponse
from django.shortcuts import render

from bank.models import Bank
from fruits.models import Fruit


# Create your views here.
def index(request):
    fruits = Fruit.objects.all()
    bank = Bank.objects.first()
    return render(request, 'main_page.html', context={'fruits': fruits, 'bank': bank})


def get_last_transactions(request):
    if request.method == 'GET':
        fruits = Fruit.objects.all()

        return JsonResponse({"success": {fruit.id: fruit.last_transaction for fruit in fruits}}, status=200)
    return JsonResponse({}, status=405)
