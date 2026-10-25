from django.contrib.auth.models import User
from django import forms

from market.models import Listing


class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ["title", "description", "price", "category", "seller_note"]


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        # is_staff is an authorization flag (desk + admin access), not a profile
        # preference. It must never be settable by the account holder, so it is
        # not listed here. Staff is granted out of band (admin / manage.py).
        fields = ["first_name", "last_name", "email"]
