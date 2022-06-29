from django.contrib import admin

from .models import Task

class TaskAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'title', 'description', 'start_date', 'end_date', 'completed', 
        'user'
    )
    list_filter = ('title','description','user','completed')
    search_fields = (
        'id', 'title', 'description', 'start_date', 'end_date', 'completed', 
        'user__username'
    )

admin.site.empty_value_display = '-void-'
admin.site.register(Task, TaskAdmin)