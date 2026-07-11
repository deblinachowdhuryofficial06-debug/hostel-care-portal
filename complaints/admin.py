
from django.contrib import admin
from .models import Complaint

# This tells the admin dashboard to display our Complaint table
admin.site.register(Complaint)
# Register your models here.
