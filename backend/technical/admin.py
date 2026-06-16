from django.contrib import admin
from .models import Document, TechnicalReport

admin.site.register(Document)
admin.site.register(TechnicalReport)