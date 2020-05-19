from django.contrib import admin
from script import models

# Register your models here.

class PostAdmin(admin.ModelAdmin):
    list_display = ['script_name','script_methods','script_path','service_name','server_name']

admin.site.register(models.script_data,PostAdmin)
admin.site.register(models.all_parameter)
admin.site.register(models.script_status)
# Register your models here.
