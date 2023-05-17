from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View


# Create your views here.
class CustomLoginView(View):
    success_url = reverse_lazy("start_page")

    def post(self, request):
        user = authenticate(
            self.request,
            username=request.POST.get("username"),
            password=request.POST.get("password"),
        )
        if user is not None:
            login(self.request, user)
            messages.success(request, f'Hello {request.POST.get("username")}')
            return redirect(self.success_url)
        messages.error(request, "Incorrect username or password")
        return redirect(self.success_url)


class CustomLogoutView(View):
    success_url = reverse_lazy("start_page")

    def get(self, request):
        if self.request.user.is_authenticated:
            logout(request)
        return redirect(self.success_url)
