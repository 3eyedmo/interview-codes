from django.db import models
from variants.models import VariantsModel


class MahmooleModel(models.Model):
    MAHMOOLE_TYPE_CHOICES = (
        ("depo", "depo"),
        ("order", "order")
    )
    pid = models.CharField(max_length=128, null=True)
    date = models.DateField(null=True)
    mahmoole_type = models.CharField(max_length=255, choices=MAHMOOLE_TYPE_CHOICES, null=True)

    def __str__(self) -> str:
        return self.pid + "-" + str(self.date)



class OrderModel(models.Model):
    variant = models.ForeignKey(
        VariantsModel,
        on_delete=models.SET_NULL,
        related_name="orders",
        null=True
    )
    order_number = models.PositiveIntegerField()
    mahmoole = models.ForeignKey(MahmooleModel, on_delete=models.SET_NULL, null=True, related_name="orders")
    dkpc = models.CharField(max_length=127, null=True)

    class Meta:
        ordering = ("-mahmoole__date",)

    def __str__(self) -> str:
        return self.variant.product.title + f"(number={self.order_number})"
