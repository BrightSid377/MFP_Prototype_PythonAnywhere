from django.contrib import admin
from .models import Customer, OrdersHeader, Demographics, PickupLocation, OrderLine, Products, Staff, Dependent, Comment

# Register your models here
admin.site.register(Customer)
admin.site.register(OrdersHeader)
admin.site.register(Demographics)
admin.site.register(PickupLocation)
admin.site.register(OrderLine)
admin.site.register(Products)
admin.site.register(Staff)
admin.site.register(Dependent)
admin.site.register(Comment)

