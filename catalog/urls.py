from django.urls import path
from . import views
from .views import OrdersListView, OrderCreate, OrderDetailView, OrderLineCreate, FulfillmentUpdate, FulfillmentView

urlpatterns = [
    path('', views.index, name='index'),
    path('orders/', OrdersListView.as_view(), name='order_list'),  # List all orders
    path('order/new/', OrderCreate.as_view(), name='order_create'),  # Create a new order
    path('order/<int:pk>/', OrderDetailView.as_view(), name='order_detail'),
    path('order/<int:pk>/orderline_create/', OrderLineCreate.as_view(), name='orderline_create'), # View details of a specific order

#     path('catalog/order_list/', views.OrdersListView.as_view(), name='order_list'),
# # mjl 7/31/2024 working on orderline page
#     path('orderline/create/', views.OrderLineCreate.as_view(), name='orderline_create'),
#     path('orderline/<int:pk>/update/', views.OrderLineUpdate.as_view(), name='orderline_update'),
# # mjl 7/30/2024 adding rows here for new order page
#     path('order/create/', views.OrderCreate.as_view(), name='order_create'),
#     path('order/<int:pk>/update/', views.OrderUpdate.as_view(), name='order_update'),

# mjl 7/31/2024 adding rows here for new staff and products page
    path('products/create/', views.ProductsCreate.as_view(), name='products_create'),
    path('products/<int:pk>/update/', views.ProductsUpdate.as_view(), name='products_update'),
    path('products/<int:pk>/delete/', views.products_delete, name='products_delete'),
    path('catalog/products_list/', views.ProductsListView.as_view(), name='products_list'),

    path('staff/create/', views.StaffCreate.as_view(), name='staff_create'),
    path('staff/<int:pk>/update/', views.StaffUpdate.as_view(), name='staff_update'),
    path('staff/<int:pk>/delete/', views.staff_delete, name='staff_delete'),
    path('catalog/staff_list/', views.StaffListView.as_view(), name='staff_list'),

    # ar 7/31 adding url route for profile page
    path('profile/', views.profile, name='profile'),
    #ar 8/5/2024 adding edit_profile view
    path('profile/edit/', views.edit_profile, name='edit_profile'),

    #ar 8/1 adding demogrpahics form view
    path('demographics_form/', views.demographics_form, name='demographics_form'),

    #for order fulfillment page
    path('orders_list/', views.orders_list, name='orders'),
    # mjl 8/10/2024 added for fulfillment page
    path('fulfillment/', views.FulfillmentView.as_view(), name='fulfillment'),
    path('fulfillment/<int:pk>/update/', views.FulfillmentUpdate.as_view(), name='fulfillment_update'),

]