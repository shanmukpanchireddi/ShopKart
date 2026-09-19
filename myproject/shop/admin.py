from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from django import forms
from .models import Catog, Product
from cloudinary.uploader import upload

# Custom form to handle image URL uploads
class ProductAdminForm(forms.ModelForm):
    prod_image_url = forms.URLField(required=False, label="Image URL (for Cloudinary)")

    class Meta:
        model = Product
        fields = '__all__'

    def save(self, commit=True):
        instance = super().save(commit=False)

        # If a URL is provided, upload it to Cloudinary
        url = self.cleaned_data.get('prod_image_url')
        if url:
            result = upload(url)
            instance.prod_image = result['public_id']

        if commit:
            instance.save()
        return instance

# ✅ Category Admin (unchanged)
@admin.register(Catog)
class CatogAdmin(ImportExportModelAdmin):
    list_display = ['name', 'status', 'created_at']

# ✅ Product Admin
@admin.register(Product)
class ProductAdmin(ImportExportModelAdmin):
    form = ProductAdminForm
    list_display = ['name', 'vendor', 'catof', 'quantity', 'selling_price', 'status', 'created_at']

    # This line is CRUCIAL to make both fields appear
    fields = [
        'catof',
        'name',
        'vendor',
        'prod_image',       # File input (default Django field)
        'prod_image_url',   # Custom URL input field (added via ModelForm)
        'quantity',
        'original_price',
        'selling_price',
        'desc',
        'status',
        'trending',
    ]
