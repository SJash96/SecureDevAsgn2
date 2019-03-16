from django.contrib import admin

from .models import Threads

class MyAdmin(admin.ModelAdmin):
    def has_delete_permission(self, request, obj=None):
        return False
    def has_add_permission(self, request):
        return False
    def save_model(self, request, obj, form, change):
        pass

admin.site.register(Threads, MyAdmin)
admin.site.site_header = "Administration"
