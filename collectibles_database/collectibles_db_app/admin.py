from django.contrib import admin
from . import models


class  CollectibleItemAdmin(admin.ModelAdmin):
    model = models. CollectibleItem
    list_display = ('user', 'country', 'currency', 'release_year', 'circulation', 
                    'item_type', 'denomination', 'quantity', 'condition', 'description', 
                    'register_date', 'update_date')
    list_filter = ('country', 'item_type', 'user' )
    search_fields = ('country', 'currency', 'item_type',)


admin.site.register(models.CollectibleItem, CollectibleItemAdmin)
