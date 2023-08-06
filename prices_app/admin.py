from django.contrib import admin
from . import models
# Register your models here.


class SymbolAdmin(admin.ModelAdmin):
    list_display = ["id", "symbol", "is_active", "icon"]
    list_editable = ["symbol", "is_active", "icon"]
    list_filter = ["is_active"]
    search_fields = ["symbol"]
    ordering = ["id"]


admin.site.register(models.Symbol, SymbolAdmin)
