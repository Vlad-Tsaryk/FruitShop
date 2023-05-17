from django.urls import path

from fruits.views import index, get_last_transactions

urlpatterns = [
    path("", index, name="start_page"),
    path("get_last_transactions/", get_last_transactions, name="get_last_transactions"),
]
