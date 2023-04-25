from django.core.management.base import BaseCommand
from orders.make_orders import get_json, save_to_db
from pathlib import Path


class Command(BaseCommand):
    help = 'Create a new orders'
    # py manage.py create_order -f final_orders or final_orders.json

    def add_arguments(self, parser):
        parser.add_argument('-f', '--filename', type=str, help="Filename that should be writen in database.")

    def handle(self, *args, **options):
        filename = options.get("filename")
        base_name = "orders/order_jsons/"
        if ".json" in filename:
            final_path = base_name + filename
        else:
            final_path = base_name + filename + ".json"
        
        final_path = Path(final_path)
        if final_path.exists():
            self.stdout.write(self.style.SUCCESS("the path is : " + str(final_path)))
            data = get_json(filename=final_path)
            save_to_db(data=data)
        else:
            self.stdout.write(self.style.ERROR("the path is not correct!!"))
