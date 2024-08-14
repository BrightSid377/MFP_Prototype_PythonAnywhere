from django import forms
from .models import Demographics, Profile, OrderLine, PickupLocation
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import OrdersHeader, Products
from django.forms import modelformset_factory # mjl 8/10/2024 added to resolve error after merge

def validate_age(value):
    try:
        age = int(value)
    except ValueError:
        raise ValidationError('Age must be a valid integer.')

    if not (0 <= age <= 120):
        raise ValidationError('Age must be between 0 and 120.')

def validate_NUID(value):
    if not value.isdigit() or len(value) != 8:  # Adjust length as per your requirement
        raise ValidationError('NUID must be a 8-digit number.')

def validate_zip_code(value):
    import re
    if not re.match(r'^\d{5}(-\d{4})?$', value):
        raise ValidationError('Enter a valid ZIP code.')

class DemographicsForm(forms.ModelForm):
    class Meta:
        model = Demographics
        fields = ['user_id', 'user_secondary_email','user_NUID','user_grad','user_affiliation',
                  'is_international_student','is_first_gen', 'user_class_standing',
                  'user_transportation', 'user_living_status', 'user_transportation',
                  'user_occupation', # mjl 8/10/2024 added occupation field which was missing
                  'user_employment',
                  'user_ethnicity', 'user_age', 'user_gender_identity', 'user_marital_status',
                  'has_dependents', 'user_number_dependents', 'user_wgec', 'user_zip_code', 'user_allergies',
                  'user_household_size',]
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(DemographicsForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['user_id'].initial = user.id
            self.fields['user_id'].widget = forms.HiddenInput()

        self.fields['user_age'].validators.append(validate_age)
        self.fields['user_NUID'].validators.append(validate_NUID)
        self.fields['user_zip_code'].validators.append(validate_zip_code)
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'image', 'private']

class OrderCreateForm(forms.ModelForm):
    products = forms.ModelMultipleChoiceField(
        queryset=Products.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    quantities = forms.CharField(
        widget=forms.HiddenInput(),  # Hide the field from the user
        required=False
    )
    pickup_location_id = forms.ModelChoiceField(
        queryset=PickupLocation.objects.all(),
        label="Pickup Location",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    class Meta:
        model = OrdersHeader
        fields = ['pickup_location_id', 'order_date', 'order_fill_or_shop', 'is_bag_required', 'order_diapers', 'order_parent_supplies', 'order_notes']
    def clean(self):
        cleaned_data = super().clean()
        products = cleaned_data.get('products')
        quantities = cleaned_data.get('quantities')
        if products and not quantities:
            raise forms.ValidationError("Quantities must be provided for selected products.")
        # Parse quantities
        if quantities:
            quantities = quantities.split(',')
            if len(products) != len(quantities):
                raise forms.ValidationError("Mismatch between products and quantities.")
        return cleaned_data

class OrderLineForm(forms.ModelForm):
    class Meta:
        model = OrderLine
        fields = ['product_id', 'order_line_number', 'order_quantity_requested' ] #, 'order_notes']
        # widgets = {
        #     'order_notes': forms.Textarea(attrs={'rows': 3}),
        # }
        # mjl 8/10/2024 removing order notes to resolve merge conflict
OrderLineFormSet = modelformset_factory(OrderLine, fields=('product_id', 'order_quantity_requested'), extra=1)
