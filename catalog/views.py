from django.urls import reverse_lazy

from .models import (OrdersHeader,Products, Staff, User, OrderLine, Order)
#, Valueform)
from django.shortcuts import render, reverse, resolve_url, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect
from .forms import DemographicsForm, OrderCreateForm
from django.views import generic
from django.views.generic.detail import DetailView
from .forms import OrderLineForm
# mjl 7/31/2024 added for email functionality
# https://www.geeksforgeeks.org/setup-sending-email-in-django-project/
# https://www.youtube.com/watch?v=5Iumyy3d2eA
from django.conf import settings
from django.core.mail import send_mail
from django.views.generic import ListView

def index(request):
    """View function for home page of site."""
    num_customers = User.objects.all().count()

    # num_instances = BookInstance.objects.all().count()
    # Available books (status = 'a')
    # num_instances_available = BookInstance.objects.filter(status__exact='a').count()\
    # The 'all()' is implied by default.
    # num_authors = Author.objects.count()
    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1
    context = {
        'num_customers': num_customers,
    #    'num_instances': num_instances,
    #    'num_instances_available': num_instances_available,
    #    'num_authors': num_authors,
        'num_visits': num_visits,
    }
    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)

# # mjl 7/31/2024 create orderline page
#
# class OrderLineCreate(CreateView):
#     model = OrderLine
#     fields = ['order_line_number', 'order_quantity_requested', 'order_notes','order_id','product_id']
#     def get_success_url(self):
#         return reverse('orderline_create')  # redirects customer to page after commiting change
#     # should have this redirect to order details to continue entries
#
# class OrderLineUpdate(UpdateView):
#     model = OrderLine
#     fields = ['order_line_number', 'order_quantity_requested', 'order_notes','order_id','product_id']
#     def get_success_url(self):
#         return reverse('orderline_create') # redirects customer to page after commiting change
#     # should have this redirect to order details to continue entries

class OrdersListView(LoginRequiredMixin, ListView):
    model = OrdersHeader
    template_name = 'catalog/order_list.html'
    context_object_name = 'orders'
    paginate_by = 10
    def get_queryset(self):
        # Filter orders by the logged-in user
        return OrdersHeader.objects.filter(user_id=self.request.user).order_by('-order_date')

class OrderCreate(LoginRequiredMixin, CreateView):
    model = OrdersHeader
    form_class = OrderCreateForm
    template_name = 'catalog/order_create.html'
    def form_valid(self, form):
        # Automatically assign the current user to the order
        form.instance.user_id = self.request.user

        response = super().form_valid(form)

        # Create OrderLine instances
        # self.create_order_lines(form)

        return response
    # didn't end up needing but might utilize in a later update.
    # def create_order_lines(self, form):
    #     # Extract product IDs and quantities
    #     products = form.cleaned_data.get('products')
    #     quantities = form.cleaned_data.get('quantities')
    #
    #     if products and quantities:
    #         quantities = quantities.split(',')
    #
    #         # Create each OrderLine instance
    #         for product, quantity in zip(products, quantities):
    #             OrderLine.objects.create(
    #                 order_id=self.object,  # Link the OrderLine to the created OrdersHeader instance
    #                 product_id=product,
    #                 order_line_number=f'{self.object.order_id:03}',  # You might want to generate a unique line number
    #                 order_quantity_requested=quantity,
    #                 order_notes=''  # Or include logic for handling notes if provided
    #             )

    def get_success_url(self):
        # Redirect to the order details page after creation
        return reverse('order_detail', kwargs={'pk': self.object.pk})


class OrderDetailView(LoginRequiredMixin, DetailView):
    model = OrdersHeader
    template_name = 'catalog/order_detail.html'
    context_object_name = 'order'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order_lines'] = self.object.orderline_set.all()  # Fetch related order lines
        return context

class OrderLineCreateView(CreateView):
    model = OrderLine
    form_class = OrderLineForm
    template_name = 'catalog/orderlines_form.html'  # Template for creating an order line

    def form_valid(self, form):
        # Set the order_id from the URL parameter
        form.instance.order_id = OrdersHeader.objects.get(pk=self.kwargs['order_pk'])
        return super().form_valid(form)

    def get_success_url(self):
        # Redirect to the order detail page after creation
        return reverse_lazy('order_detail', kwargs={'pk': self.kwargs['order_pk']})

# mjl 7/31/2024 adding staff and product entry views


class ProductsUpdate(UpdateView):
    model = Products
    fields = ['product_name', 'product_description', 'product_availability','product_quantity']
    def get_success_url(self):
        return reverse('order_list') # redirects customer to page after commiting change

class ProductsCreate(CreateView):
    model = Products
    fields = ['product_name', 'product_description', 'product_availability','product_quantity']
    def get_success_url(self):
        return reverse('order_list')  # redirects customer to page after commiting change

class ProductsListView(LoginRequiredMixin,generic.ListView):
    model = Products
    template_name = 'catalog/products_list.html'
    paginate_by = 10


class StaffUpdate(UpdateView):
    model = Staff
    fields = ['staff_first_name', 'staff_last_name', 'staff_position']
    def get_success_url(self):
        return reverse('order_list')  # redirects customer to page after commiting change

class StaffCreate(CreateView):
    model = Staff
    fields = ['staff_first_name', 'staff_last_name', 'staff_position']
    def get_success_url(self):
        return reverse('order_list')  # redirects customer to page after commiting change

class StaffListView(LoginRequiredMixin,generic.ListView):
    model = Staff
    template_name = 'catalog/staff_list.html'
    paginate_by = 10

# mjl 7/30/2024 trying to allow customer to be chosen during order entry
# https://www.educba.com/django-foreign-key/
# def order_view(request):
#     form = Valueform(request.POST or None)  # see models.py for Valueform def
#     if form.is_valid():
#         post = form.save()
#         post.Creator = request.user
#         print('Creator user stored',request.user)
#         post.save()
#     return  render(request,'ordersheader_form.html', {"form": form})
# def order_edit(request):
#     form = Valueform(request.POST or None)
#     if form.is_valid():
#         post = form.save()
#         post.Creator = request.user
#         print('Creator user updated',request.user)
#         post.save()
#     return  render(request,'ordersheader_form_edit.html', {"form": form})
# def order_update(request):
#     form = Valueform(request.POST or None)
#     if form.is_valid():
#         post = form.save()
#         post.Creator = request.user
#         print('Creator user updated',request.user)
#         post.save()
#     return  render(request,'ordersheader_form_edit.html', {"form": form})

@login_required
def profile(request):
    user = request.user  # Get the current logged-in user
    profile, created = Profile.objects.get_or_create(user=user)
    demographics = get_object_or_404(Demographics, user_id=user)

    context = {
        'user': user,
        'profile': profile,
        'demographics': demographics,
    }
    return render(request, 'catalog/profile.html', context)
# mjl 7/31/2024 adding delete features for staff and products
def staff_delete(request, pk):
    staff = get_object_or_404(Staff, pk=pk)
    try:
        staff.delete()
        messages.success(request, (staff.staff_first_name + ' ' +
                                   staff.staff_last_name +" has been deleted"))
    except:
        messages.success(request, (staff.staff_first_name + ' ' + staff.staff_last_name + ' cannot be deleted.'))
    return redirect('order_list')

def products_delete(request, pk):
    products = get_object_or_404(Products, pk=pk)
    try:
        products.delete()
        messages.success(request, (Products.product_name +" has been deleted"))
    except:
        messages.success(request, (Products.product_name + ' cannot be deleted.'))
    return redirect('order_list')

# mjl 7/31/2024 looking to send emails based on fulfillment date
# def send_customer_notification():
#     subject = 'Maverick Food Pantry - Order Ready'
#     message = f'Hi {User.first_name}, your requested Order is ready for pickup.'
#     email_from = settings.EMAIL_HOST_USER
#     recipient_list = 'mjl07734@gmail.com' #[User.email, ]
#     send_mail(subject, message, email_from, recipient_list)

# https://stackoverflow.com/questions/59406326/django-sending-email-using-signals
#
# from .models import Booking
#
# @receiver(post_save, sender=Booking)
# def new_booking(sender, instance, **kwargs):
# if instance.firstname:
#     firstname = (instance.firstname)
#     email = (instance.email)
#     subject = (instance.service)
#     send_mail(firstname, subject, email,
#               ['cmadiam@abc.com'], fail_silently=False)


@login_required
def demographics_form(request):
    if request.method == 'POST':
        form = DemographicsForm(request.POST, user=request.user)
        if form.is_valid():
            demographics = form.save(commit=False)
            demographics.user = request.user  # Ensure the user is set correctly
            demographics.save()
            messages.success(request, 'Demographics information submitted successfully!')
            return redirect('index')  # Adjust redirect as needed
    else:
        form = DemographicsForm(user=request.user)

    return render(request, 'demographics_form.html', {'form': form})

#ar 8/05/2024 adding profile edit view

from .forms import UserForm, ProfileForm, DemographicsForm
from .models import Profile, Demographics

@login_required
def edit_profile(request):
    user = request.user
    profile, created = Profile.objects.get_or_create(user=user)
    demographics, created = Demographics.objects.get_or_create(user_id=user)

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
        demographics_form = DemographicsForm(request.POST, instance=demographics)

        if user_form.is_valid() and profile_form.is_valid() and demographics_form.is_valid():
            user_form.save()
            profile_form.save()
            demographics_form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        user_form = UserForm(instance=user)
        profile_form = ProfileForm(instance=profile)
        demographics_form = DemographicsForm(instance=demographics)

    return render(request, 'catalog/edit_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'demographics_form': demographics_form
    })

def orders(request):
    packing_orders = Order.objects.filter(status=Order.PACKING)
    current_orders = Order.objects.filter(status=Order.PICKUP)
    old_orders = Order.objects.filter(status=Order.RETURNS)

    context = {
        'packing_orders': packing_orders,
        'current_orders': current_orders,
        'old_orders': old_orders,
    }

    return render(request, 'orders.html', context)