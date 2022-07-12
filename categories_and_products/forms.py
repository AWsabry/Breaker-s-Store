
from email.policy import default
from django import forms


class QuantityForm(forms.Form):
    Quantity = forms.IntegerField(min_value=1,initial=1)

    def clean(self):
        cleaned_data = super(QuantityForm, self).clean()
        return cleaned_data

    # def clean(self,*args,**kwargs):
    #     Quantity = self.cleaned_data.get("Quantity")
    #     if not Quantity is None :
    #         raise forms.ValidationError("Quantity should be at least 1 ")
    #     if Quantity == 0:
    #         raise forms.ValidationError("Quantity should be at least 1")
      
    #     return super(QuantityForm,self).clean(*args,**kwargs)