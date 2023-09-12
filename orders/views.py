from django.views import generic

from orders.models import Order


class OrderListView(generic.ListView):
    model = Order
    queryset = Order.objects.select_related("employee")
