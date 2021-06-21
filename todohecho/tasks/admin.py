from django.contrib import admin
from .models import Task, Priority


# Register your models here.

class TaskAdmin(admin.ModelAdmin):
    list_display = ('title','author','description','completed_date','created_date',)
    search_fields = ('title','author__username')
    filter_horizontal=()
    list_filter=()
    fieldsets=()
    readonly_fields = ('created_date',)

admin.site.register(Task,TaskAdmin)
admin.site.register(Priority)