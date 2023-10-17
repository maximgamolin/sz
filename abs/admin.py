from django.contrib import admin


class BaseModelAdmin(admin.ModelAdmin):
    list_display = ['version', 'is_deleted', 'updated_at', 'created_at']

    class Meta:
        abstract = True
