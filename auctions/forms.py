from django import forms


class CreateListingForm(forms.Form):
    title = forms.CharField(
        label="Title:",
        required=True,
        widget=forms.TextInput(attrs={
            "class": "form-control"
        })
    )
    description = forms.CharField(
        label="Description:",
        required=True,
        widget=forms.Textarea(attrs={
            "class": "form-control",
            "row": "5"
        })
    )
    bid = forms.IntegerField(
        label="Starting Bid:",
        required=True,
        widget=forms.NumberInput(attrs={
            "class": "form-control"
        })
    )
    image_url = forms.URLField(
        label="URL to Listing Image:",
        required=False,
        widget=forms.TextInput(attrs={
            "class": "form-control"
        })
    )
    category = forms.CharField(
        label="Category:",
        required=False,
        widget=forms.TextInput(attrs={
            "class": "form-control"
        })
    )
