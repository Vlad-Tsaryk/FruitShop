from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone

from bank.models import Bank, Declaration
from fruits.models import Fruit
from users.models import Message


# Create your views here.
def index(request):
    fruits = Fruit.objects.all()
    bank = Bank.objects.first()
    messages = Message.objects.all()[:40][::-1]
    declarations_today = Declaration.objects.filter(date=timezone.now()).count()
    return render(
        request,
        "main_page.html",
        context={"fruits": fruits, "bank": bank, "messages": messages, 'declarations_today': declarations_today},
    )


def get_last_transactions(request):
    if request.method == "GET":
        fruits = Fruit.objects.all()
        return JsonResponse(
            {"success": {fruit.id: fruit.last_transaction for fruit in fruits}},
            status=200,
        )
    return JsonResponse({}, status=405)
