from django.contrib import admin
from script import models

# Register your models here.

class PostAdmin(admin.ModelAdmin):
    list_display = ['script_name','script_path','service_name','server_name','status']

admin.site.register(models.script_data,PostAdmin)
admin.site.register(models.all_parameter)
# Register your models here.
