from django import forms  
from AppOnlineTransactionFraudDetection.models import User_details

class UserDetailsForm(forms.ModelForm):  
    class Meta:  
        model = User_details  
        fields = "__all__"  

