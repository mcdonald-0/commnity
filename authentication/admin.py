from django.contrib import admin

from authentication.models import *

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ('username',)
    prepopulated_fields = {'slug': ('username',)} 


admin.site.register(User, UserAdmin)
