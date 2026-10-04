from django import forms
from .models import Cars, Review


class CarsForm(forms.ModelForm):
    class Meta:
        model = Cars
        fields = (
            "category",
            "name",
            "price",
            "short_description",
            "description",
            "stock",
            "is_active",
            "main_image",
        )


class ReviewForm(forms.ModelForm):
    rating = forms.ChoiceField(
        choices=[(i, "★" * i) for i in range(1, 6)]
    )

    comment = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                "rows": 4,
                "placeholder": "Izoh ..... (ixtiyoriy)",
            }
        ),
    )

    class Meta:
        model = Review
        fields = ("rating", "comment")
