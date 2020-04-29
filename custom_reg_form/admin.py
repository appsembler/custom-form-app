from django.contrib import admin
from .models import ExtraInfo


class ExtraInfoAdmin(admin.ModelAdmin):
    list_display = ('user',)
    search_fields = ('user',)


admin.site.register(ExtraInfo, ExtraInfoAdmin)
