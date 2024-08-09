from django.contrib import admin
from .models import OrdersHeader, Demographics, PickupLocation, OrderLine, Products, Staff, Dependent, Comment

# mjl 7/30/2024 ======= new =======
# https://docs.djangoproject.com/en/5.0/topics/auth/customizing/#extending-user
# trying to associate a registered user to Customer
# from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# from django.contrib.auth.models import User
#
# class CustomerInline(admin.StackedInline):
#     model = Customer
#     can_delete = False
#     verbose_name_plural = "customer"
#
# # Define a new User admin
# class UserAdmin(BaseUserAdmin):
#     inlines = [CustomerInline]
#
# # Re-register UserAdmin
# admin.site.unregister(User)
# admin.site.register(User, UserAdmin)
# ====== end new === mjl 7/30/2024


# Register your models here
# admin.site.register(Customer)
admin.site.register(OrdersHeader)
admin.site.register(Demographics)
admin.site.register(PickupLocation)
admin.site.register(OrderLine)
admin.site.register(Products)
admin.site.register(Staff)
admin.site.register(Dependent)
admin.site.register(Comment)

