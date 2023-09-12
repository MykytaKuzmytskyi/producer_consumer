import datetime

from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views import generic
from django_celery_beat.models import PeriodicTask
from orders.tasks import send_telegram

from orders.models import Order
from producer_consumer.settings import NAME_CREATE_ORDERS_TASK


class OrderListView(generic.ListView):
    model = Order

    def get_queryset(self):
        queryset = Order.objects.select_related("employee").filter(
            employee=self.request.user
        )
        return queryset


class OrderDeleteView(generic.DeleteView):
    model = Order
    success_url = reverse_lazy("orders:order-list")

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.delete()
        send_telegram.delay(
            f"Задача №{self.object.name.split()[1]} під назвою {self.object.name}"
            f" була опрацьована працівником {self.object.employee.first_name}"
            f" у {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )
        return HttpResponseRedirect(success_url)


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
