from django import forms
from .models import ShippingInfo

class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'placeholder': '姓名',
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'placeholder': '電子郵件',
        })
    )
    phone = forms.CharField(
        max_length=15,
        widget=forms.TextInput(attrs={
            'placeholder': '電話號碼',
        })
    )
    question = forms.CharField(
        max_length=500,
        widget=forms.TextInput(attrs={
            'placeholder': '提問內容',
        })
    )

class ShippingInfoForm(forms.ModelForm):
    class Meta:
        model = ShippingInfo
        fields = ['recipient_name', 'address', 'phone_number', 'email']