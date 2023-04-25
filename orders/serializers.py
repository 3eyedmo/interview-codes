from rest_framework import serializers
from variants.models import VariantsModel, FamilyModel, ColorModel
from panels.models import PanelModel, BoxModel
from orders.models import OrderModel
from jdatetime import date as jd


class FamilyForOrderModel(serializers.ModelSerializer):
    class Meta:
        model = FamilyModel
        fields = ["en_name"]

    def to_representation(self, instance):
        return super().to_representation(instance).get("en_name")


class ColorForOrderModel(serializers.ModelSerializer):
    class Meta:
        model = ColorModel
        fields = ["name"]

    def to_representation(self, instance):
        return super().to_representation(instance).get("name")


class PanelForOrderModel(serializers.ModelSerializer):
    class Meta:
        model = PanelModel
        fields = ["fa_name"]

    def to_representation(self, instance):
        return super().to_representation(instance).get("fa_name")


class BoxForOrderModel(serializers.ModelSerializer):
    class Meta:
        model = BoxModel
        fields = ["en_name"]

    def to_representation(self, instance):
        return super().to_representation(instance).get("en_name")


class VariantSerializer(serializers.ModelSerializer):
    color = ColorForOrderModel()
    families = FamilyForOrderModel(source="product.familly")
    panel = PanelForOrderModel()
    title = serializers.CharField(source="product.title")
    dkp = serializers.CharField(source="product.dkp")
    box = serializers.CharField(source="product.box.en_name")
    brand = serializers.CharField(source="product.brand")
    model = serializers.CharField(source="product.model")

    class Meta:
        model = VariantsModel
        fields = ("id", "color", "families", "panel", "dkpc", "quentity", "is_active", "seller_stock", "title", "waranty", "dkp", "box", "brand", "model")

    def to_representation(self, instance):
        data = super().to_representation(instance)
        
        if hasattr(instance, "quantity_sum"):
            if instance.quantity_sum is None:
                data["quantity_sum"] = 0
            else:
                data["quantity_sum"] = instance.quantity_sum
        
        return data


class OrderSerializer(serializers.ModelSerializer):
    variant = VariantSerializer()
    date = serializers.DateField(source="mahmoole.date")
    kind = serializers.CharField(source="mahmoole.mahmoole_type")
    class Meta:
        model = OrderModel
        fields = ("dkpc", "order_number", "date", "kind", "variant", )
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        initial_date = data["date"].split("-")
        data["date"] = str(jd.fromgregorian(
            day=int(initial_date[2]),
            month=int(initial_date[1]),
            year=int(initial_date[0])
        ))
        return data
