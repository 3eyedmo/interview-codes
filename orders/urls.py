from django.urls import path
from . import views


app_name = "orders"
urlpatterns = [
    path("", views.OrderView.as_view(), name="orders"),
    path("most_selled/", view=views.MostSelledView.as_view(), name="most_selled")
]