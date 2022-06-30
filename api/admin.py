from django.contrib import admin

from .models import Task

class TaskAdmin(admin.ModelAdmin):
    empty_value_display = '-void-'
    list_display = (
        'id', 'title', 'description', 'start_date', 'end_date', 'completed', 
        'user'
    )
    list_filter = ('title','description','user','completed')
    readonly_fields = ('id',)
    search_fields = (
        'id', 'title', 'description', 'start_date', 'end_date', 'completed', 
        'user__username'
    )
    

admin.site.register(Task, TaskAdmin)