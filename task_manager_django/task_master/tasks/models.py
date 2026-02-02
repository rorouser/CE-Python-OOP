from django.db import models
from django.contrib.auth.models import User
import datetime
from django.core.exceptions import ValidationError


class Project(models.Model):
    title = models.CharField(max_length=200, verbose_name="Título")
    description = models.TextField(verbose_name="Descripción")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    deadline = models.DateField(verbose_name="Fecha límite")
    owner = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='owned_projects',
        verbose_name="Propietario"
    )
    collaborators = models.ManyToManyField(
        User, 
        related_name='collaborated_projects', 
        blank=True,
        verbose_name="Colaboradores"
    )

    class Meta:
        verbose_name = "Proyecto"
        verbose_name_plural = "Proyectos"
        ordering = ['-created_at']

    def __str__(self):
        return self.title
    
    def clean(self):
        """Validación: la deadline no puede ser una fecha pasada"""
        if self.deadline and self.deadline < datetime.date.today():
            raise ValidationError({'deadline': 'La fecha límite no puede ser una fecha pasada.'})
    
    def get_task_stats(self):
        """Devuelve estadísticas de las tareas del proyecto"""
        total_tasks = self.tasks.count()
        done_tasks = self.tasks.filter(status='DONE').count()
        todo_tasks = self.tasks.filter(status='TODO').count()
        in_progress_tasks = self.tasks.filter(status='INPROG').count()
        
        return {
            'total': total_tasks,
            'done': done_tasks,
            'todo': todo_tasks,
            'in_progress': in_progress_tasks,
            'done_percentage': (done_tasks / total_tasks * 100) if total_tasks > 0 else 0,
            'pending_percentage': ((total_tasks - done_tasks) / total_tasks * 100) if total_tasks > 0 else 0
        }


class Task(models.Model):
    STATUS_CHOICES = [
        ('TODO', 'Pendiente'),
        ('INPROG', 'En Progreso'),
        ('DONE', 'Completada'),
    ]
    PRIORITY_CHOICES = [
        ('L', 'Baja'),
        ('M', 'Media'),
        ('H', 'Alta'),
    ]
    
    project = models.ForeignKey(
        Project, 
        on_delete=models.CASCADE, 
        related_name='tasks',
        verbose_name="Proyecto"
    )
    title = models.CharField(max_length=200, verbose_name="Título")
    description = models.TextField(blank=True, verbose_name="Descripción")
    status = models.CharField(
        max_length=6, 
        choices=STATUS_CHOICES, 
        default='TODO',
        verbose_name="Estado"
    )
    priority = models.CharField(
        max_length=1, 
        choices=PRIORITY_CHOICES, 
        default='M',
        verbose_name="Prioridad"
    )
    assigned_to = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='assigned_tasks',
        verbose_name="Asignado a"
    )

    class Meta:
        verbose_name = "Tarea"
        verbose_name_plural = "Tareas"
        ordering = ['-priority', 'status']

    def __str__(self):
        return f"{self.title} ({self.project.title})"
    
    def get_priority_display_color(self):
        """Devuelve un color Bootstrap basado en la prioridad"""
        colors = {
            'L': 'success',
            'M': 'warning',
            'H': 'danger'
        }
        return colors.get(self.priority, 'secondary')
    
    def get_status_display_color(self):
        """Devuelve un color Bootstrap basado en el estado"""
        colors = {
            'TODO': 'secondary',
            'INPROG': 'primary',
            'DONE': 'success'
        }
        return colors.get(self.status, 'secondary')
