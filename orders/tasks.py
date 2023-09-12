import random

import requests
from celery import shared_task
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models import Max
from django.db.models.functions import Coalesce

from orders.models import Order


def get_random_model():
    max_id = get_user_model().objects.all().aggregate(max_id=Max("id"))["max_id"]
    while True:
        pk = random.randint(1, max_id)
        employee = get_user_model().objects.filter(pk=pk).first()
        if employee:
            return employee


@shared_task
def create_order():
    employee = get_random_model()
    max_id = Order.objects.all().aggregate(max_id=Coalesce(Max("pk"), 0))["max_id"]
    order = Order.objects.create(
        name=f"Order {1 + max_id}",
        description=f"Description {1 + max_id}",
        employee=employee,
    )
    return dict(order_id=order.pk)


@shared_task
def send_telegram(text: str):
    token = settings.TOKEN
    url = "https://api.telegram.org/bot"
    chat_id = settings.SHAT_ID
    url += token
    method = url + "/sendMessage"

    req = requests.post(method, data={"chat_id": chat_id, "text": text})

    if req.status_code != 200:
        raise ValueError
