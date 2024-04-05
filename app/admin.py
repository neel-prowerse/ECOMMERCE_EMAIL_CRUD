from django.contrib import admin

# Register your models here.
from .models import Mobile,Company,Cart,Order
admin.site.register(Mobile)
admin.site.register(Company)
admin.site.register(Cart)
admin.site.register(Order)
