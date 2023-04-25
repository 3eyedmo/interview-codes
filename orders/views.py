from django.db.models import Sum
from django.db.models.functions import Coalesce

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination

from variants.models import VariantsModel
from orders.serializers import VariantSerializer, OrderSerializer
from orders.models import OrderModel

from jdatetime import date as jd


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000



def get_en_date(fa_date: str):
    print(fa_date)
    f = fa_date.split("/")
    date = jd(
        year=int(f[0]),
        month=int(f[1]),
        day=int(f[2])
    ).togregorian()
    return date


def get_parameter(request):
    queries = dict()
    families = request.query_params.get("families")
    boxes = request.query_params.get("boxes")
    brands = request.query_params.get("brands")
    panels = request.query_params.get("panels")
    kind = request.query_params.get("kind")
    colors = request.query_params.get("colors")
    from_date = request.query_params.get("from_date")
    to_date = request.query_params.get("to_date")

    if families:
        queries.update({
            "variant__product__familly__main_famillies__en_name__in": families.split(",")
        })
    if boxes:
        queries.update({
            "variant__product__box__en_name__in": boxes.split(",")
        })
    if brands:
        queries.update({
            "variant__product__brand__in": brands.split(",")
        })
    if panels:
        queries.update({
            "variant__panel__en_name__in": panels.split(",")
        })
    if kind:
        queries.update({
            "mahmoole__mahmoole_type__in": kind.split(",")
        })
    if colors:
        queries.update({
            "variant__color__name__in": colors.split(",")
        })
        print(colors.split(","))
    if from_date:
        queries.update({
            "mahmoole__date__gte": get_en_date(from_date)
        })
    if to_date:
        queries.update({
            "mahmoole__date__lte": get_en_date(to_date)
        })
    return queries


def most_selled_parameter(request):
    queries = dict()
    families = request.query_params.get("families")
    boxes = request.query_params.get("boxes")
    brands = request.query_params.get("brands")
    panels = request.query_params.get("panels")
    colors = request.query_params.get("colors")
    from_date = request.query_params.get("from_date")
    to_date = request.query_params.get("to_date")

    if families:
        queries.update({
            "product__familly__main_famillies__en_name__in": families.split(",")
        })
    if boxes:
        queries.update({
            "product__box__en_name__in": boxes.split(",")
        })
    if brands:
        queries.update({
            "product__brand__in": brands.split(",")
        })
    if panels:
        queries.update({
            "panel__en_name__in": panels.split(",")
        })
    if colors:
        queries.update({
            "color__name__in": colors.split(",")
        })
        print(colors.split(","))
    if from_date:
        queries.update({
            "orders__mahmoole__date__gte": get_en_date(from_date)
        })
    if to_date:
        queries.update({
            "orders__mahmoole__date__lte": get_en_date(to_date)
        })
    return queries


class OrderView(ListAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = OrderSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        queries = get_parameter(self.request)
        if queries:
            return OrderModel.objects.filter(**queries)
        return OrderModel.objects.all()


class MostSelledView(ListAPIView):
    serializer_class = VariantSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        most_selled_queries: dict = most_selled_parameter(self.request)
        if most_selled_queries:
            qs = VariantsModel.objects.filter(
                **most_selled_queries
            ).annotate(quantity_sum=Coalesce(Sum('orders__order_number'), 0)).order_by("-quantity_sum")
        else:
            qs = VariantsModel.objects.annotate(quantity_sum=Coalesce(
                Sum('orders__order_number'), 0)).order_by("-quantity_sum")
        return qs
