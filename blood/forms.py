from django import forms

from . import models


class BloodForm(forms.ModelForm):
    class Meta:
        model=models.Stock
        fields=['bloodgroup','unit']

class RequestForm(forms.ModelForm):
    class Meta:
        model=models.BloodRequest
        fields=['patient_name','patient_age','reason','bloodgroup','unit','rbc','wbc']
        
        
class contactForm(forms.ModelForm):
    
    class Meta:
        model=models.contact
        fields=['first_name','last_name','age','bloodgroup','disease','doctorname','address','mobile']
