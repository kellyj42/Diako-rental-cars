from django import forms
from django.core.validators import MinValueValidator
from datetime import date
from cars.models import Car

class BookingForm(forms.Form):
    # Car Selection
    car_id = forms.IntegerField(widget=forms.HiddenInput())
    car_name = forms.CharField(widget=forms.HiddenInput(), required=False)
    
    # Location Details
    pick_up_location = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'placeholder': 'City or Airport',
            'class': 'form-control'
        }),
        required=True
    )
    
    drop_off_location = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'placeholder': 'City or Airport',
            'class': 'form-control'
        }),
        required=True
    )
    
    # Date & Time
    pick_up_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        validators=[MinValueValidator(date.today())]
    )
    
    pick_up_time = forms.TimeField(
        widget=forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
        required=True
    )
    
    drop_off_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        validators=[MinValueValidator(date.today())]
    )
    
    drop_off_time = forms.TimeField(
        widget=forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
        required=True
    )
    
    # Customer Details
    full_name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=20, required=True)
    
    # Additional Info
    additional_notes = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 4,
            'placeholder': 'Special requests, child seats, etc.',
            'class': 'form-control'
        }),
        required=False
    )
    
    # Terms Agreement
    agree_terms = forms.BooleanField(
        required=True,
        error_messages={'required': 'You must agree to the terms and conditions'}
    )
    
    def clean(self):
        cleaned_data = super().clean()
        pick_up_date = cleaned_data.get('pick_up_date')
        drop_off_date = cleaned_data.get('drop_off_date')
        
        if pick_up_date and drop_off_date:
            if drop_off_date < pick_up_date:
                raise forms.ValidationError("Drop-off date must be after pick-up date.")
            
            # Calculate duration
            duration = (drop_off_date - pick_up_date).days
            if duration < 1:
                raise forms.ValidationError("Minimum rental period is 1 day.")
        
        return cleaned_data