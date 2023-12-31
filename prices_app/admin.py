from django.contrib import admin
from . import models


# Register your models here.


class SymbolAdmin(admin.ModelAdmin):
    list_display = ["symbol", "is_popular", "icon"]
    list_editable = ["is_popular", "icon"]
    list_filter = ["is_popular"]
    search_fields = ["symbol"]
    ordering = ["id"]


admin.site.register(models.Symbol, SymbolAdmin)
