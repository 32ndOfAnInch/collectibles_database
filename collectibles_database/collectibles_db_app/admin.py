from django.contrib import admin
from . import models


class  CollectibleItemAdmin(admin.ModelAdmin):
    model = models. CollectibleItem
    list_display = ('user', 'country', 'currency', 'release_year', 'circulation', 
                    'item_type', 'denomination', 'quantity', 'condition', 'description', 
                    'register_date', 'update_date')
    list_filter = ('country', 'item_type' )
    search_fields = ('country', 'currency', 'item_type',)


class GradingSystemAdmin(admin.ModelAdmin):
    model = models.GradingSystem
    list_display = ('name',  'description', 'condition')


admin.site.register(models.CollectibleItem, CollectibleItemAdmin)
admin.site.register(models.Condition)
admin.site.register(models.GradingSystem, GradingSystemAdmin)
