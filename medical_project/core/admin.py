from django.contrib import admin
from .models import Medicine, Bill
# Register your models here.

admin.site.register(Medicine)
admin.site.register(Bill)