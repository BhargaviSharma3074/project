from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Product

class UserRegistrationForm(UserCreationForm):
    """User registration form"""
    email = forms.EmailField(required=False)
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['first_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})
        
        # Remove password validation - allow any password
        self.fields['password1'].validators = []
        self.fields['password2'].validators = []
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None
    
    def clean_password2(self):
        """Override to only check if passwords match, no other validation"""
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("The two password fields didn't match.")
        return password2

class ProductForm(forms.ModelForm):
    """Product form for adding/updating products"""
    class Meta:
        model = Product
        fields = ['name', 'product_id', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'product_id': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }
        labels = {
            'name': 'Product Name',
            'product_id': 'Product ID (Unique Code)',
            'description': 'Product Description',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product_id'].help_text = 'Enter a unique identification code for this product'

