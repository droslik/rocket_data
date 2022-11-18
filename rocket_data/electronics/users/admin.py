from django.contrib import admin
from .models import User, UserAPIKey
from electronics.tasks import populate_db_with_celery


def create_fake_data(self, request, queryset):
    """Admin action to populate Database with fake data"""
    return populate_db_with_celery.delay()


create_fake_data.short_description = 'Populate Database with data'


class UserAdmin(admin.ModelAdmin):
    actions = [create_fake_data, ]


admin.site.register(User, UserAdmin)
admin.site.register(UserAPIKey)



