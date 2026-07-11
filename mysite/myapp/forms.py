from django import forms
from django.contrib.auth.models import User
from .models import UserProfile, Review

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['address', 'city', 'state', 'zip_code', 'country', 'phone_number', 'card_name', 'card_number_last_four']
        labels = {
            'card_number_last_four': 'Card Number (last 4 digits)'
        }

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.Select(attrs={'class': 'form-control'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Write your comments here...'}),
        }