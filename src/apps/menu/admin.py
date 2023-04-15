from django.contrib import admin
from .models import Menu


class MenuAdmin(admin.ModelAdmin):
    list_display = ('title', 'parent', 'slug')
    search_fields = ('title',)
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Menu, MenuAdmin)


