from django.contrib import admin
from orders.models import OrderModel, MahmooleModel


@admin.register(OrderModel)
class OrderModelAdmin(admin.ModelAdmin):
    list_display = [
        "variant", "order_number", "mahmoole", "dkpc"
    ]

@admin.register(MahmooleModel)
class MahmooleModelAdmin(admin.ModelAdmin):
    list_display = [
        "pid", "date", "mahmoole_type"
    ]
