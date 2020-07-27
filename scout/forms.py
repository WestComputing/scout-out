import re

from django import forms


class LocationForm(forms.Form):
    zip_code = forms.CharField(max_length=5, required=False)
    city = forms.CharField(max_length=50, required=False)
    state = forms.CharField(max_length=2, required=False)
    label = forms.CharField(max_length=50, required=False)

    def clean(self):
        cleaned_data = super().clean()
        zip_code = cleaned_data.get("zip_code")
        city = cleaned_data.get("city")
        state = cleaned_data.get("state")
        if zip_code:
            if re.match(r"\d{5}", zip_code) is None:
                raise forms.ValidationError("Zip code must be 5 digits")
        elif city and state:
            if len(state) != 2:
                raise forms.ValidationError("State must be two letters")
        else:
            raise forms.ValidationError("Must fill in zip code or city and state")
