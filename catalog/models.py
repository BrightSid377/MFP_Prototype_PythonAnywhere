from django.db import models
from django.urls import reverse # used to generate URLs by reversing the URL patterns
import uuid

# Create your models here

class Customer(models.Model):
    customer_id = models.AutoField(primary_key=True)
    demographics_id = models.ForeignKey('Demographics', on_delete=models.CASCADE)
    customer_first_name = models.CharField(max_length=50)
    customer_last_name = models.CharField(max_length=50)
    customer_email = models.EmailField(unique=True)
    customer_phone_number = models.CharField(max_length=12)

    FACULTY_OR_STAFF_CHOICES = [
        ('Y', 'Yes'),
        ('N', 'No'),
    ]
    is_faculty_or_staff = models.CharField(max_length=1, choices=FACULTY_OR_STAFF_CHOICES)

    def get_full_customer_info(self):
        return {
            "customer_id": self.customer_id,
            "demographics_id": self.demographics_id,
            "customer_first_name": self.customer_first_name,
            "customer_last_name": self.customer_last_name,
            "customer_email": self.customer_email,
            "customer_phone_number": self.customer_phone_number,
            "faculty_or_staff": self.get_is_faculty_or_staff_display()
        }
class OrdersHeader(models.Model):
    order_id = models.AutoField(primary_key=True)
    customer_id = models.ForeignKey('Customer', on_delete=models.CASCADE)
    pickup_location_id = models.ForeignKey('PickupLocation', on_delete=models.CASCADE)
    order_date = models.DateField()
    order_fill_or_shop = models.CharField(max_length=20)

    IS_BAG_REQUIRED_CHOICES = [
        ('Y', 'Yes'),
        ('N', 'No'),
    ]
    is_bag_required = models.CharField(max_length=1, choices=IS_BAG_REQUIRED_CHOICES)
    order_fulfillment_date = models.DateField()

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

    def get_full_ordersheader_info(self):
        return {
            "order_id": self.order_id,
            "customer_id": self.customer_id,
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
            "order_parent_supplies": self.get_order_parent_supplies_display()
        }

class Demographics(models.Model):
    demographics_id = models.AutoField(primary_key=True)
    customer_id = models.ForeignKey('Customer', on_delete=models.CASCADE)
    dependent_id = models.ForeignKey('Dependent', on_delete=models.CASCADE)
    comment_id = models.ForeignKey('Comment', on_delete=models.CASCADE)
    customer_secondary_email = models.EmailField(unique=True, null=True)
    customer_NUID = models.CharField(max_length=20, null=True, default='0')

    CUSTOMER_GRAD_CHOICES = [
        ('Y', 'Yes'),
        ('N', 'No'),
    ]
    customer_grad = models.CharField(max_length=1, choices=CUSTOMER_GRAD_CHOICES)
    customer_affiliation = models.CharField(max_length=50, null=True)

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

    CUSTOMER_CLASS_STANDING_CHOICES = [
        ('1', 'Freshman'),
        ('2', 'Sophomore'),
        ('3', 'Junior'),
        ('4', 'Senior'),
    ]
    customer_class_standing = models.CharField(max_length=1, choices=CUSTOMER_CLASS_STANDING_CHOICES, null=True)
    customer_occupation = models.CharField(max_length=50)
    customer_living_status = models.CharField(max_length=200)
    customer_transportation = models.CharField(max_length=150)

    CUSTOMER_EMPLOYMENT_CHOICES = [
        ('Y', 'Yes'),
        ('N', 'No'),
    ]
    customer_employment = models.CharField(max_length=1, choices=CUSTOMER_EMPLOYMENT_CHOICES)
    customer_ethnicity = models.CharField(max_length=50)
    customer_age = models.CharField(max_length=2)
    customer_gender_identity = models.CharField(max_length=100)

    CUSTOMER_MARITAL_STATUS_CHOICES = [
        ('Y', 'Yes'),
        ('N', 'No'),
    ]
    customer_marital_status = models.CharField(max_length=1, choices=CUSTOMER_MARITAL_STATUS_CHOICES)
    customer_household_size = models.CharField(max_length=50)

    HAS_DEPENDENTS_CHOICES = [
        ('Y', 'Yes'),
        ('N', 'No'),
    ]
    has_dependents = models.CharField(max_length=1, choices=HAS_DEPENDENTS_CHOICES)
    customer_number_dependents = models.CharField(null=True, max_length=50)

    CUSTOMER_WGEC_CHOICES = [
        ('Y', 'Yes'),
        ('N', 'No'),
    ]
    customer_wgec = models.CharField(max_length=1, choices=CUSTOMER_WGEC_CHOICES)
    customer_zip_code = models.CharField(max_length=10)
    customer_allergies = models.CharField(max_length=50)

    def get_full_demographic_info(self):
        return {
            "customer_id": self.customer_id,
            "customer_secondary_email": self.customer_secondary_email,
            "customer_NUID": self.customer_NUID,
            "customer_grad": self.get_customer_grad_display(),
            "customer_affiliation": self.customer_affiliation,
            "is_international_student": self.get_is_international_student_display(),
            "is_first_gen": self.get_is_first_gen_display(),
            "customer_class_standing": self.get_customer_class_standing_display(),
            "customer_occupation": self.customer_occupation,
            "customer_living_status": self.customer_living_status,
            "customer_transportation": self.customer_transportation,
            "customer_employment": self.get_customer_employment_display(),
            "customer_ethnicity": self.customer_ethnicity,
            "customer_age": self.customer_age,
            "customer_gender_identity": self.customer_gender_identity,
            "customer_marital_status": self.get_customer_marital_status_display(),
            "customer_household_size": self.customer_household_size,
            "has_dependents": self.get_has_dependents_display(),
            "customer_number_dependents": self.customer_number_dependents,
            "customer_wgec": self.get_customer_wgec_display(),
            "customer_zip_code": self.customer_zip_code,
            "customer_allergies": self.customer_allergies
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

class OrderLine(models.Model):
    order_id = models.ForeignKey('OrdersHeader', on_delete=models.CASCADE)
    product_id = models.ForeignKey('Products', on_delete=models.CASCADE)
    order_line_number = models.CharField(max_length=100)
    order_quantity_requested = models.CharField(max_length=100)
    order_notes = models.TextField(null=True, blank=True)

    def get_full_orderline_info(self):
        return {
            "order_id": self.order_id,
            "product_id": self.product_id,
            "order_line_number": self.order_line_number,
            "order_quantity_requested": self.order_quantity_requested,
            "order_notes": self.order_notes
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

class Staff(models.Model):
    staff_id = models.AutoField(primary_key=True)
    staff_first_name = models.CharField(max_length=50)
    staff_last_name = models.CharField(max_length=50)
    staff_position = models.CharField(max_length=50)

    def get_full_staff_info(self):
        return {
            "staff_id": self.staff_id,
            "staff_first_name": self.staff_first_name,
            "staff_last_name": self.staff_last_name,
            "staff_position": self.staff_position
        }

class Dependent(models.Model):
    dependent_id = models.AutoField(primary_key=True)
    dependent_age = models.IntegerField(null=True, blank=True)

    def get_full_dependent_info(self):
        return {
            "dependent_id": self.dependent_id,
            "dependent_age": self.dependent_age
        }

class Comment(models.Model):
    comment_id = models.AutoField(primary_key=True)
    comment_comment = models.TextField(null=True, blank=True)

    def get_full_comment_info(self):
        return {
            "comment_id": self.comment_id,
            "comment_comment": self.comment_comment
        }