from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin
from catalog.models import Demographics


class DemographicsMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.user.is_authenticated:
            try:
                # Get the customer information associated with the logged-in user
                user = User.objects.get(id=request.user.pk)

                # Check to see if the authenticated customer has filled out their demographics information
                if not Demographics.objects.filter(user_id=request.user.pk).exists():
                    # Avoid redirect loop by excluding the demographics and logout paths
                    if request.path not in [reverse('demographics_form'), reverse('logout')]:
                        return redirect('demographics_form')
            except User.DoesNotExist:
                return redirect('register')