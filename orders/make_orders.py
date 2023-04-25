import json
from pathlib import Path
from variants.models import VariantsModel
from orders.models import OrderModel, MahmooleModel
from jdatetime import date as jd


def get_json(filename):
    with open(filename, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data

mah_type = {
    "سفارش":"order",
    "انبارش":"depo"
}

def get_or_none(dkpc):
    try:
        variant = VariantsModel.objects.get(dkpc = dkpc)
    except:
        variant = None
    return variant

def save_to_db(data):
    for item in data:
        package_data = item.get("package_data")
        pid = package_data.get("pid")
        status = package_data.get("status")
        j_mahdate = package_data.get("date").split("/")
        mah_date = jd(year=int(j_mahdate[0]), month=int(j_mahdate[1]), day=int(j_mahdate[2])).togregorian()
        kind = mah_type.get(package_data.get("kind"))
        
        if status == "حذف شده":
            continue
        
        print(mah_date)
        mahmoole, _ = MahmooleModel.objects.get_or_create(
            pid=pid,
            date=mah_date,
            mahmoole_type=kind,
        )
        package_orders = item.get("data")
        for order_item in package_orders:
            dkpc = order_item.get("dkpc")
            variant = get_or_none(dkpc=dkpc)
            order_count = order_item.get("order")
            if mahmoole:
                OrderModel.objects.create(
                    variant=variant,
                    order_number=order_count,
                    mahmoole=mahmoole,
                    dkpc=dkpc,
                )
            else:
                OrderModel.objects.create(
                    variant=variant,
                    order_number=order_count,
                    dkpc=dkpc,
                )
