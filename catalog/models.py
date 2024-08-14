from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.urls import reverse # used to generate URLs by reversing the URL patterns
import uuid

# Create your models here

class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE, unique=True)
    # first_name = models.TextField(max_length=500, null=True, blank=True)
    # last_name = models.TextField(max_length=500, null=True, blank=True)
    # email = models.TextField(max_length=500, null=True, blank=True)
    bio = models.TextField(max_length=500, null=True, blank=True)
    image = models.ImageField(upload_to="images/profile",
                              default="images/profile/default.png", null=True)
    private = models.BooleanField(default=True)

    def __str__(self):
        return str(self.user)

# class Customer(models.Model):
#     customer_id = models.AutoField(primary_key=True)
#     # mjl 7/30/2024 need to connect registered user to customer account trying foreign key
#     # https://docs.djangoproject.com/en/5.0/topics/auth/customizing/#extending-user
#     user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
#     # demographics_id = models.ForeignKey('Demographics', on_delete=models.CASCADE)
#     customer_first_name = models.CharField(max_length=50)
#     customer_last_name = models.CharField(max_length=50)
#     customer_email = models.EmailField(unique=True)
#     customer_phone_number = models.CharField(max_length=12)
#
#     FACULTY_OR_STAFF_CHOICES = [
#         ('Y', 'Yes'),
#         ('N', 'No'),
#     ]
#     is_faculty_or_staff = models.CharField(max_length=1, choices=FACULTY_OR_STAFF_CHOICES)

    # def get_full_customer_info(self):
    #     return {
    #         "customer_id": self.customer_id,
    #         "demographics_id": self.demographics_id,
    #         "customer_first_name": self.customer_first_name,
    #         "customer_last_name": self.customer_last_name,
    #         "customer_email": self.customer_email,
    #         "customer_phone_number": self.customer_phone_number,
    #         "faculty_or_staff": self.get_is_faculty_or_staff_display()
    #     }
class OrdersHeader(models.Model):
    order_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # mjl 8/10/2024 adding join to staff so we can assign them to orders
    staff_id = models.ForeignKey('Staff', null = True, on_delete=models.CASCADE)
    # @property  # mjl 8/10/2024 trying this in place of above code
    # def staff_id(self):
    #         return f"{self.staff_id.staff_first_name}"

    pickup_location_id = models.ForeignKey('PickupLocation', on_delete=models.CASCADE)
    order_date = models.DateField()
    # order_fill_or_shop = models.CharField(max_length=20)  mjl 7/30/2024 updating to list
    FILL_SHOP_CHOICES = [
        ('fill','Please pack my order for me'),
        ('shop',"I'll shop in store"),
    ]
    order_fill_or_shop = models.CharField(max_length=4, choices=FILL_SHOP_CHOICES)

    IS_BAG_REQUIRED_CHOICES = [
        ('Y', 'Yes please bag for me'),
        ('N', "No I'll bring my own"),
    ]
    is_bag_required = models.CharField(max_length=1, choices=IS_BAG_REQUIRED_CHOICES)
    # mjl 7/30/2024 adding null allowed so customer can enter new order without fulfillment date
    order_fulfillment_date = models.DateField(blank=True, null=True)
    ORDER_PICKUP_STATUS_CHOICES = [
        ('Y', 'Yes'),
        ('N', 'No'),
    ]
    order_pickup_status = models.CharField(max_length=1, choices=ORDER_PICKUP_STATUS_CHOICES)
    order_notification_date_1st = models.DateField(blank=True, null=True)
    order_notification_date_2nd = models.DateField(blank=True, null=True)
    order_notification_date_3rd = models.DateField(blank=True, null=True)
    ORDER_DIAPERS_CHOICES = [
        ('Y', 'Yes'),
        ('N', 'No'),
    ]
    order_diapers = models.CharField(max_length=1, choices=ORDER_DIAPERS_CHOICES)

    ORDER_PARENT_SUPPLIES_CHOICES = [
        ('Y', 'Yes'),
        ('N', 'No'),
    ]
    order_parent_supplies = models.CharField(max_length=1, choices=ORDER_PARENT_SUPPLIES_CHOICES)
    # mjl 8/10/2024 moved up from orderline
    order_notes = models.TextField(null=True, blank=True)
    def get_full_ordersheader_info(self):
        return {
            "order_id": self.order_id,
            "User_id": self.user_id,
            "staff_id": self.staff_id,
            "pickup_location_id": self.pickup_location_id,
            "order_date": self.order_date,
            "order_fill_or_shop": self.order_fill_or_shop,
            "is_bag_required": self.get_is_bag_required_display(),
            "order_fulfillment_date": self.order_fulfillment_date,
            "order_pickup_status": self.get_order_pickup_status_display(),
            "order_notification_date_1st": self.order_notification_date_1st,
            "order_notification_date_2nd": self.order_notification_date_2nd,
            "order_notification_date_3rd": self.order_notification_date_3rd,
            "order_diapers": self.get_order_diapers_display(),
            "order_parent_supplies": self.get_order_parent_supplies_display(),
            "order_notes": self.order_notes
        }

class Demographics(models.Model):
    demographics_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    # dependent_id = models.ForeignKey('Dependent', on_delete=models.CASCADE)
    # comment_id = models.ForeignKey('Comment', on_delete=models.CASCADE)
    # Changes to our ERD design made these foreign keys not necessary
    user_secondary_email = models.EmailField(unique=True, null=True, default='None')
    user_NUID = models.CharField(max_length=20, null=True, default='0')

    USER_GRAD_CHOICES = [
        ('Y', 'Yes'),
        ('N', 'No'),
    ]
    user_grad = models.CharField(max_length=1, choices=USER_GRAD_CHOICES)

    USER_AFFILIATION_CHOICES = [
        ('1', 'UNO'),
        ('2', 'UNMC'),
        ('3', 'MCC'),
    ]
    user_affiliation = models.CharField(max_length=1, choices=USER_AFFILIATION_CHOICES, null=True)

    IS_INTERNATIONAL_STUDENT_CHOICES = [
        ('Y', 'Yes'),
        ('N', 'No'),
    ]
    is_international_student = models.CharField(max_length=1, choices=IS_INTERNATIONAL_STUDENT_CHOICES)

    IS_FIRST_GEN_CHOICES = [
        ('Y', 'Yes'),
        ('N', 'No'),
    ]
    is_first_gen = models.CharField(max_length=1, choices=IS_FIRST_GEN_CHOICES)

    USER_CLASS_STANDING_CHOICES = [
        ('1', 'Freshman'),
        ('2', 'Sophomore'),
        ('3', 'Junior'),
        ('4', 'Senior'),
    ]
    user_class_standing = models.CharField(max_length=1, choices=USER_CLASS_STANDING_CHOICES, null=True)

    # mjl 8/10/2024 adding occupation field
    user_occupation = models.CharField(max_length=100, null=True)

    USER_LIVING_STATUS_CHOICES = [
        ('1', 'Off-Campus - alone'),
        ('2', 'Off-campus - With Family'),
        ('3', 'On-Campus'),
    ]
    user_living_status = models.CharField(max_length=1, choices=USER_LIVING_STATUS_CHOICES, null=True)

    USER_TRANSPORTATION_CHOICES = [
        ('1', 'Walking'),
        ('2', 'Public Transportation'),
        ('3', 'Car'),
    ]
    user_transportation = models.CharField(max_length=1, choices=USER_TRANSPORTATION_CHOICES, null=True)

    USER_EMPLOYMENT_CHOICES = [
        ('1', 'Part-Time'),
        ('2', 'Full-Time'),
        ('3', 'Not Employed'),
        ('4', 'Unable to Work')
    ]
    user_employment = models.CharField(max_length=1, choices=USER_EMPLOYMENT_CHOICES)

    # mjl 8/10/2024 updating to a choice field
    USER_ETHNICITY_CHOICES = [
        ('1', 'Black or African American'),
        ('2', 'White or Caucasian'),
        ('3', 'Hispanic or Latinx'),
        ('4', 'American Indian or Alaskan'),
        ('5', 'Asian'),
        ('6', 'Prefer Not to Say'),
    ]
    user_ethnicity = models.CharField(max_length=1, choices=USER_ETHNICITY_CHOICES)

    user_age = models.CharField(max_length=2)

    # mjl 8/10/2024 updating to a choice field
    USER_GENDER_CHOICES = [
        ('1', 'Male'),
        ('2', 'Female'),
        ('3', 'Non-Binary'),
        ('4', 'Trans'),
        ('5', 'Prefer Not to Say')
    ]
    user_gender_identity = models.CharField(max_length=1, choices=USER_GENDER_CHOICES)

    USER_MARITAL_STATUS_CHOICES = [
        ('Y', 'Yes'),
        ('N', 'No'),
    ]
    user_marital_status = models.CharField(max_length=1, choices=USER_MARITAL_STATUS_CHOICES)
    user_household_size = models.CharField(max_length=50)

    HAS_DEPENDENTS_CHOICES = [
        ('Y', 'Yes'),
        ('N', 'No'),
    ]
    has_dependents = models.CharField(max_length=1, choices=HAS_DEPENDENTS_CHOICES)
    user_number_dependents = models.CharField(null=True, max_length=50)

    USER_WGEC_CHOICES = [
        ('Y', 'Affiliated with WGEC'),
        ('N', 'No'),
    ]
    user_wgec = models.CharField(max_length=1, choices=USER_WGEC_CHOICES)
    user_zip_code = models.CharField(max_length=10)
    user_allergies = models.CharField(max_length=50)

    def get_full_demographic_info(self):
        return {
            "cuser_id": self.user_id,
            "user_secondary_email": self.user_secondary_email,
            "user_NUID": self.user_NUID,
            "user_grad": self.get_user_grad_display(),
            "user_affiliation": self.user_affiliation,
            "is_international_student": self.get_is_international_student_display(),
            "is_first_gen": self.get_is_first_gen_display(),
            "user_class_standing": self.get_user_class_standing_display(),
            "user_living_status": self.user_living_status,
            "user_transportation": self.user_transportation,
            "user_occupation": self.user_occupation, # mjl 8/10/2024 added was missing
            "user_employment": self.get_user_employment_display(),
            "user_ethnicity": self.user_ethnicity,
            "user_age": self.user_age,
            "user_gender_identity": self.user_gender_identity,
            "user_marital_status": self.get_user_marital_status_display(),
            "user_household_size": self.user_household_size,
            "has_dependents": self.get_has_dependents_display(),
            "user_number_dependents": self.user_number_dependents,
            "user_wgec": self.get_user_wgec_display(),
            "user_zip_code": self.user_zip_code,
            "user_allergies": self.user_allergies
        }

class PickupLocation(models.Model):
    pickup_location_id = models.AutoField(primary_key=True)
    pickup_location_name = models.CharField(max_length=50)
    pickup_location_address = models.CharField(max_length=20)
    pickup_location_description = models.CharField(max_length=50)

    def get_full_pickuplocation_info(self):
        return {
            "pickup_location_id": self.pickup_location_id,
            "pickup_location_name": self.pickup_location_name,
            "pickup_location_address": self.pickup_location_address,
            "pickup_location_description": self.pickup_location_description
        }

    def __str__(self):
        return self.pickup_location_name

class OrderLine(models.Model):
    # 8/10 this naming scheme can still be called else where by referencing order_id. do not change breaks order line create function
    order = models.ForeignKey('OrdersHeader', on_delete=models.CASCADE)
    product_id = models.ForeignKey('Products', on_delete=models.CASCADE)
    order_line_number = models.CharField(max_length=100)
    order_quantity_requested = models.CharField(max_length=100)
    # mjl 8/10/2024 moving to order header
    # order_notes = models.TextField(null=True, blank=True)

    # class Meta:  # mjl 7/31/2024 hopefully sorts the columns dif when displayed by form
    #         fields_order = [
    #             'order_id',
    #             'order_line_number',
    #             'product_id',
    #             'order_quantity_requested',
    #             'order_notes'
    #             ]

    def get_full_orderline_info(self):
        return {
            "order_id": self.order_id,
            "product_id": self.product_id,
            "order_line_number": self.order_line_number,
            "order_quantity_requested": self.order_quantity_requested,
        }




class Products(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=150)
    product_description = models.TextField()

    PRODUCT_AVAILABILITY_CHOICES = [
        ('Y', 'Yes'),
        ('N', 'No'),
    ]
    product_availability = models.CharField(max_length=1, choices=PRODUCT_AVAILABILITY_CHOICES)
    product_quantity = models.IntegerField()

    def get_full_products_info(self):
        return {
        "product_id": self.product_id,
        "product_name": self.product_name,
        "product_description": self.product_description,
        "product_availability": self.get_product_availability_display(),
        "product_quantity": self.product_quantity

        }
    def __str__(self):
        return self.product_name


class Staff(models.Model):
    staff_id = models.AutoField(primary_key=True)
    staff_first_name = models.CharField(max_length=50)
    staff_last_name = models.CharField(max_length=50)
    staff_position = models.CharField(max_length=50)

    def __str__(self):
        return self.staff_first_name # mjl 8/13/2024 to prevent ID showing on update screen, show name instead
    # def get_full_staff_info(self):
    #     return {
    #         "staff_id": self.staff_id,
    #         "staff_first_name": self.staff_first_name,
    #         "staff_last_name": self.staff_last_name,
    #         "staff_position": self.staff_position
    #     }


class Dependent(models.Model):
    dependent_id = models.AutoField(primary_key=True)
    demographics_id = models.ForeignKey('Demographics', on_delete=models.CASCADE, null=True)
    dependent_age = models.IntegerField(null=True, blank=True)

    def get_full_dependent_info(self):
        return {
            "dependent_id": self.dependent_id,
            "dependent_age": self.dependent_age
        }

class Comment(models.Model):
    comment_id = models.AutoField(primary_key=True)
    demographics_id = models.ForeignKey('Demographics', on_delete=models.CASCADE, null=True)
    comment_comment = models.TextField(null=True, blank=True)

    def get_full_comment_info(self):
        return {
            "comment_id": self.comment_id,
            "comment_comment": self.comment_comment
        }

class OrderComment(models.Model):
    order_comment_id = models.AutoField(primary_key=True)
    comment_id = models.ForeignKey('Comment', on_delete=models.CASCADE, null=True)
    order_comment_comment = models.TextField(null=True, blank=True)
    comment_type = models.CharField(max_length=20, null=True, blank=True)

    def get_full_comment_info(self):
        return {
            "order_comment_id": self.order_comment_id,
            "comment_comment": self.order_comment_comment,
            "comment_type": self.comment_type,
            }

# mjl 7/30/2024 trying to get Order form to allow for selection of
# customer when posting
# https://www.educba.com/django-foreign-key/
# from django import forms
# from .models import Customer
# class Valueform(forms.ModelForm):
#     class Meta:
#         model = Customer
#         fields = "__all__"

# this is for the order fulfillment page
class Order(models.Model):
    PACKING = 'For Packing'
    PICKUP = 'For Pickup'
    RETURNS = 'Returns'

    ORDER_STATUS_CHOICES = [
        (PACKING, 'For Packing'),
        (PICKUP, 'For Pickup'),
        (RETURNS, 'Returns'),
    ]

    order_id = models.AutoField(primary_key=True)
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default=PACKING)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order {self.order_id} - {self.status}"