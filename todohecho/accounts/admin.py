from django.contrib import admin
from .models import Account


from django.contrib.auth.admin import UserAdmin

# Register your models here.




class AccountAdmin(UserAdmin):
    list_display = ('email','username','date_joined','last_login','is_admin','is_staff')
    search_fields = ('email','username')
    filter_horizontal=()
    list_filter=()
    fieldsets=()
    readonly_fields = ('id','date_joined','last_login')



admin.site.register(Account,AccountAdmin)
