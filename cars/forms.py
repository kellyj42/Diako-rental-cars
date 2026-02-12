from django import forms
from .models import Car


class CarForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		for field in self.fields.values():
			base_class = "w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:outline-none"
			if field.widget.__class__.__name__ in {"CheckboxInput"}:
				field.widget.attrs.update({"class": "h-4 w-4 text-blue-600"})
			else:
				field.widget.attrs.update({"class": base_class})

	class Meta:
		model = Car
		fields = [
			"name",
			"model",
			"year",
			"category",
			"price_per_day",
			"seats",
			"doors",
			"transmission",
			"fuel_type",
			"drive_type",
			"engine_capacity",
			"color",
			"air_conditioning",
			"bluetooth",
			"gps",
			"child_seat",
			"sunroof",
			"features",
			"thumbnail",
			"is_available",
			"is_featured",
			"description",
		]
		widgets = {
			"description": forms.Textarea(attrs={"rows": 4}),
			"features": forms.Textarea(attrs={"rows": 2}),
		}
