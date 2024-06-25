from django.contrib import admin
from . import models


# Register your models here.


@admin.register(models.User)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['id', 'username']


@admin.register(models.InventoriesTypes)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(models.Inventories)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['id', 'inventry_type', 'name', 'quantity', 'unit_price']


@admin.register(models.InventoryImage)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['image']
