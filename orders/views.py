from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views import generic
from django_celery_beat.models import PeriodicTask

from orders.models import Order
from producer_consumer.settings import NAME_CREATE_ORDERS_TASK


class OrderListView(generic.ListView):
    model = Order
    queryset = Order.objects.select_related("employee")

    def get_queryset(self):
        return Order.objects.all().filter(employee=self.request.user)


class OrderDeleteView(generic.DeleteView):
    model = Order
    success_url = reverse_lazy("orders:order-list")


def activation_create_orders(request):
    period_task = get_object_or_404(
        PeriodicTask,
        name=NAME_CREATE_ORDERS_TASK,
    )
    period_task.enabled = True
    period_task.save()
    return redirect(reverse("orders:order-list"))


def deactivation_create_orders(request):
    period_task = PeriodicTask.objects.get(
        name=NAME_CREATE_ORDERS_TASK,
    )
    period_task.enabled = False
    period_task.save()
    return redirect(reverse("orders:order-list"))