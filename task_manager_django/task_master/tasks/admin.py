from django.contrib import admin
from .models import Project, Task


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'owner', 'deadline', 'created_at', 'task_count']
    list_filter = ['created_at', 'deadline', 'owner']
    search_fields = ['title', 'description']
    filter_horizontal = ['collaborators']
    date_hierarchy = 'created_at'
    
    def task_count(self, obj):
        return obj.tasks.count()
    task_count.short_description = 'Tareas'


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'project', 'status', 'priority', 'assigned_to']
    list_filter = ['status', 'priority', 'project']
    search_fields = ['title', 'description']
    list_editable = ['status', 'priority']
