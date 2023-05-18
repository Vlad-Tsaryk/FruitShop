from django.urls import path

from .views import start_audit, cash_in, cash_out, upload_declaration

urlpatterns = [
    path("start_audit/", start_audit, name="start_audit"),
    path("cash_in/", cash_in, name="cash_in"),
    path("cash_out/", cash_out, name="cash_out"),
    path("upload_declaration/", upload_declaration, name="upload_declaration"),
]
