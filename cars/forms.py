from django import forms
from .models import Car


class AddCarForm(forms.ModelForm):
    """
    Form for adding and editing a car listing.
    seller field is excluded — it gets set automatically in the view.
    """

    auction_end_time = forms.DateTimeField(
        required=False,
        widget=forms.DateTimeInput(attrs={
            'type': 'datetime-local',
            'class': 'form-control'
        }),
        help_text='Leave blank if no auction end time'
    )

    class Meta:
        model = Car
        # seller is excluded — assigned automatically from logged-in user
        fields = [
            'title', 'description', 'brand', 'model', 'year',
            'mileage', 'vehicle_type', 'fuel_type', 'condition',
            'starting_price', 'location', 'image', 'auction_end_time'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={
                'class': 'form-control', 'rows': 4
            }),
            'brand': forms.TextInput(attrs={'class': 'form-control'}),
            'model': forms.TextInput(attrs={'class': 'form-control'}),
            'year': forms.NumberInput(attrs={
                'class': 'form-control', 'min': 1900, 'max': 2025
            }),
            'mileage': forms.NumberInput(attrs={
                'class': 'form-control', 'min': 0
            }),
            'vehicle_type': forms.Select(attrs={'class': 'form-select'}),
            'fuel_type': forms.Select(attrs={'class': 'form-select'}),
            'condition': forms.Select(attrs={'class': 'form-select'}),
            'starting_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
        }