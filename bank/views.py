from django.http import JsonResponse
from django.shortcuts import render

from .models import Bank
from .tasks import task_check_warehouse


# Create your views here.
def start_audit(request):
    if request.method == "GET":
        task_check_warehouse.delay()
        return JsonResponse({}, status=200)
    return JsonResponse({}, status=400)


def cash_in(request):
    if request.method == "GET":
        bank = Bank.objects.first()
        add_money = int(request.GET.get('money'))
        bank.balance += add_money
        bank.save()
        return JsonResponse({"success": 'Balance has been successfully replenished',
                             'balance': bank.balance}, status=200)
    return JsonResponse({}, status=405)


def cash_out(request):
    if request.method == "GET":
        bank = Bank.objects.first()
        out_money = int(request.GET.get('money'))
        if bank.balance - out_money >= 0:
            bank.balance -= out_money
            bank.save()
            return JsonResponse({"success": 'Balance has been successfully replenished',
                                 'balance': bank.balance}, status=200)
        else:
            return JsonResponse({"error": 'Balance cannot be less then zero'}, status=400)
    return JsonResponse({}, status=405)
