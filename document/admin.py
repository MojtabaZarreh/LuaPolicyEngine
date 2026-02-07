from django.contrib import admin
from .models import Document, Policy

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ("id", "title")

@admin.register(Policy)
class PolicyAdmin(admin.ModelAdmin):
    list_display = ("id", "name")