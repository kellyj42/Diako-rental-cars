from django import forms
from django.core.exceptions import ValidationError
from datetime import datetime
import re
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

	# ✅ FIX #15: Validate car name/brand
	def clean_name(self):
		"""Validate car name - allow letters, numbers, spaces, hyphens"""
		value = self.cleaned_data.get("name", "").strip()

		if not value:
			raise ValidationError("Car name is required")

		if len(value) < 2:
			raise ValidationError("Car name too short (minimum 2 characters)")

		if len(value) > 200:
			raise ValidationError("Car name too long (maximum 200 characters)")

		# Allow letters, numbers, spaces, hyphens
		if not re.match(r"^[A-Za-z0-9\s\-&]+$", value):
			raise ValidationError(
				"Car name contains invalid characters. Use letters, numbers, spaces, hyphens."
			)

		# Block XSS patterns
		if re.search(r'<[^>]*>|javascript:|onclick|onerror|on\w+=', value, re.I):
			raise ValidationError("Car name contains invalid content")

		return value

	# ✅ FIX #15: Validate model
	def clean_model(self):
		"""Validate car model"""
		value = self.cleaned_data.get("model", "").strip()

		if not value:
			return value  # Optional field

		if len(value) > 100:
			raise ValidationError("Car model too long (maximum 100 characters)")

		# Allow letters, numbers, spaces, hyphens, periods
		if not re.match(r"^[A-Za-z0-9\s\-\.]+$", value):
			raise ValidationError(
				"Car model contains invalid characters"
			)

		return value

	# ✅ FIX #15: Validate year
	def clean_year(self):
		"""Validate car year is within reasonable range"""
		value = self.cleaned_data.get("year")

		if not value:
			raise ValidationError("Year is required")

		current_year = datetime.now().year
		min_year = 1990
		max_year = current_year + 1

		if value < min_year or value > max_year:
			raise ValidationError(
				f"Year must be between {min_year} and {max_year}"
			)

		return value

	# ✅ FIX #15: Validate seats and doors
	def clean_seats(self):
		"""Validate number of seats"""
		value = self.cleaned_data.get("seats")

		if value is None:
			raise ValidationError("Seats is required")

		if value < 1 or value > 8:
			raise ValidationError("Seats must be between 1 and 8")

		return value

	def clean_doors(self):
		"""Validate number of doors"""
		value = self.cleaned_data.get("doors")

		if value is None:
			raise ValidationError("Doors is required")

		if value < 2 or value > 5:
			raise ValidationError("Doors must be between 2 and 5")

		return value

	# ✅ FIX #15: Validate price
	def clean_price_per_day(self):
		"""Validate daily rental price"""
		value = self.cleaned_data.get("price_per_day")

		if value is None:
			raise ValidationError("Price per day is required")

		if value < 0:
			raise ValidationError("Price cannot be negative")

		if value <= 0:
			raise ValidationError("Price must be greater than 0")

		if value > 99999.99:
			raise ValidationError("Price too high (maximum 99,999.99)")

		return value

	# ✅ FIX #15: Validate color and engine
	def clean_color(self):
		"""Validate color field"""
		value = self.cleaned_data.get("color", "").strip()

		if not value:
			return value  # Optional

		if len(value) > 50:
			raise ValidationError("Color too long")

		if not re.match(r"^[A-Za-z\s\-]+$", value):
			raise ValidationError("Color contains invalid characters")

		return value

	def clean_engine_capacity(self):
		"""Validate engine capacity"""
		value = self.cleaned_data.get("engine_capacity", "").strip()

		if not value:
			return value  # Optional

		if len(value) > 50:
			raise ValidationError("Engine capacity too long")

		# Allow numbers, decimal points, units (L, CC, etc)
		if not re.match(r"^[0-9\.\s\-LCcl]+$", value):
			raise ValidationError("Engine capacity contains invalid characters")

		return value

	# ✅ FIX #15: Sanitize text areas
	def clean_description(self):
		"""Sanitize description for XSS"""
		text = self.cleaned_data.get("description", "").strip()

		if not text:
			return text

		if len(text) > 2000:
			raise ValidationError("Description too long (maximum 2000 characters)")

		# Block HTML tags
		if re.search(r'<[^>]*>', text):
			raise ValidationError("HTML tags not allowed in description")

		# Block script patterns
		if re.search(r'javascript:|onclick|onerror|on\w+=', text, re.I):
			raise ValidationError("Suspicious content in description")

		return text

	def clean_features(self):
		"""Sanitize features field"""
		text = self.cleaned_data.get("features", "").strip()

		if not text:
			return text

		if len(text) > 500:
			raise ValidationError("Features too long (maximum 500 characters)")

		# Block HTML
		if re.search(r'<[^>]*>', text):
			raise ValidationError("HTML tags not allowed in features")

		# Block scripts
		if re.search(r'javascript:|onclick|onerror|on\w+=', text, re.I):
			raise ValidationError("Suspicious content in features")

		return text
