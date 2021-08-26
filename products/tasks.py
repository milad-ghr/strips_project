from api_connections.strips_connections import StripConnection
from strips.celery import app

from .models import Product


# todo: handle related image of product
@app.task(name='products.discover_tasks_from_strips')
def discover_tasks_from_strips():
    strip_connection_object = StripConnection()
    product_list = strip_connection_object.get_products()
    for product in product_list:
        product_obj, created = Product.objects.update_or_create(product_id=product['id'],
                                                                defaults={
                                                                    "name": product['name'],
                                                                    "description": product['description'],
                                                                    "active": product["active"]
                                                                })
        response = strip_connection_object.get_prices_with_product_id(product_id=product_obj.product_id)
        product_obj.price_unit = response['currency']
        product_obj.price = response['unit_amount']
        product_obj.duration_unit = response['recurring']['interval']
        product_obj.duration = response['recurring']['interval_count']
        product_obj.price_id = response['id']
        product_obj.save()



