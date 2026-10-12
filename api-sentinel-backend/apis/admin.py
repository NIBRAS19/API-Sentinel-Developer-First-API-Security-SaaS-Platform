from django.contrib import admin
from .models import Environment,APIService,Endpoint,AuthProfile
admin.site.register([Environment,APIService,Endpoint,AuthProfile])
