from django.core.cache import cache
from django.core.cache import cache
from django.http import JsonResponse
from django.shortcuts import redirect

from .models import Bank, Declaration
from .tasks import task_check_warehouse


# Create your views here.
def start_audit(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            user_id = request.user.id
            if cache.get(f"user_{user_id}") is None:
                cache.set(f"user_{user_id}", 1)
                task_check_warehouse.delay(user_id)
                return JsonResponse({}, status=200)

        return JsonResponse({}, status=400)
    return JsonResponse({}, status=405)


def cash_in(request):
    if request.method == "GET":
        bank = Bank.objects.first()
        add_money = int(request.GET.get("money"))
        bank.balance += add_money
        bank.save()
        return JsonResponse(
            {
                "success": "Balance has been successfully replenished",
                "balance": bank.balance,
            },
            status=200,
        )
    return JsonResponse({}, status=405)


def cash_out(request):
    if request.method == "GET":
        bank = Bank.objects.first()
        out_money = int(request.GET.get("money"))
        if bank.balance - out_money >= 0:
            bank.balance -= out_money
            bank.save()
            return JsonResponse(
                {
                    "success": "Balance has been successfully replenished",
                    "balance": bank.balance,
                },
                status=200,
            )
        else:
            return JsonResponse(
                {"error": "Balance cannot be less then zero"}, status=400
            )
    return JsonResponse({}, status=405)


def upload_declaration(request):
    if request.method == "POST":
        file = request.FILES.get('file')
        if file:
            Declaration.objects.create(
                file=file
            )
    return redirect('start_page')
