from django.contrib import admin
from .models import Finding,Evidence,FindingComment,FindingStatusHistory
admin.site.register([Finding,Evidence,FindingComment,FindingStatusHistory])
