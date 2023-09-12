from django.contrib import admin

from orders.models import Order, Employee

admin.site.register(Order)
admin.site.register(Employee)
