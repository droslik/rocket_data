from django.contrib import admin
from .models import Entity, Contact, Address, EntityType
from electronics.tasks import clear_debt_celery


def clear_debt(self, request, queryset):
    """Admin action clearing the debt of selected entities
    if number of selected entities less or equal to 20
    otherwise task is performed by celery task manager"""
    if len(queryset) > 20:
        entities_id = [entity.pk for entity in queryset]
        return clear_debt_celery.delay(entities_id)
    for entity in queryset:
        entity.debt = 0
        entity.save()


clear_debt.short_description = 'Clear the debt of Selected Entities'


class EntityAdmin(admin.ModelAdmin):
    lookup = 'contact__address__city'

    def lookup_allowed(self, lookup, value):
        return True

    actions = [clear_debt, ]
    list_display = ['name', 'supplier']
    list_filter = ['contact__address__city', ]
    list_display_links = ['name', 'supplier']


admin.site.register(Entity, EntityAdmin)
admin.site.register(Contact)
admin.site.register(Address)
admin.site.register(EntityType)

