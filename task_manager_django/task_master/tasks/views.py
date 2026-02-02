from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Q, Count
from .models import Project, Task
from .forms import ProjectForm, TaskForm, TaskStatusForm, RegisterForm


# Vista de registro
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, '¡Registro exitoso! Bienvenido a TaskMaster.')
            return redirect('dashboard')
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})


# Dashboard - Vista principal con "Mis Proyectos" y "Colaboraciones"
class DashboardView(LoginRequiredMixin, ListView):
    model = Project
    template_name = 'tasks/dashboard.html'
    context_object_name = 'projects'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        # Mis Proyectos (donde soy owner)
        owned_projects = Project.objects.filter(owner=user).annotate(
            task_count=Count('tasks'),
            done_count=Count('tasks', filter=Q(tasks__status='DONE'))
        )
        
        # Colaboraciones (donde soy colaborador pero no owner)
        collaborated_projects = Project.objects.filter(
            collaborators=user
        ).exclude(owner=user).annotate(
            task_count=Count('tasks'),
            done_count=Count('tasks', filter=Q(tasks__status='DONE'))
        )
        
        context['owned_projects'] = owned_projects
        context['collaborated_projects'] = collaborated_projects
        return context


# Vista de detalle del proyecto con gráfico
class ProjectDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Project
    template_name = 'tasks/project_detail.html'
    context_object_name = 'project'
    
    def test_func(self):
        """Solo el owner y colaboradores pueden ver el proyecto"""
        project = self.get_object()
        return (self.request.user == project.owner or 
                self.request.user in project.collaborators.all())
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = self.get_object()
        
        # Obtener estadísticas para el gráfico
        context['stats'] = project.get_task_stats()
        
        # Determinar si el usuario es owner
        context['is_owner'] = self.request.user == project.owner
        
        # Tareas agrupadas por estado
        context['todo_tasks'] = project.tasks.filter(status='TODO')
        context['inprogress_tasks'] = project.tasks.filter(status='INPROG')
        context['done_tasks'] = project.tasks.filter(status='DONE')
        
        return context


# Crear proyecto
class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'tasks/project_form.html'
    success_url = reverse_lazy('dashboard')
    
    def form_valid(self, form):
        form.instance.owner = self.request.user
        messages.success(self.request, 'Proyecto creado exitosamente.')
        return super().form_valid(form)


# Editar proyecto (solo owner)
class ProjectUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'tasks/project_form.html'
    
    def test_func(self):
        """Solo el owner puede editar"""
        project = self.get_object()
        return self.request.user == project.owner
    
    def get_success_url(self):
        messages.success(self.request, 'Proyecto actualizado exitosamente.')
        return reverse_lazy('project_detail', kwargs={'pk': self.object.pk})


# Eliminar proyecto (solo owner)
class ProjectDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Project
    template_name = 'tasks/project_confirm_delete.html'
    success_url = reverse_lazy('dashboard')
    
    def test_func(self):
        """Solo el owner puede eliminar"""
        project = self.get_object()
        return self.request.user == project.owner
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Proyecto eliminado exitosamente.')
        return super().delete(request, *args, **kwargs)


# Crear tarea
@login_required
def task_create(request, project_pk):
    project = get_object_or_404(Project, pk=project_pk)
    
    # Verificar permisos: owner o colaborador
    if request.user != project.owner and request.user not in project.collaborators.all():
        messages.error(request, 'No tienes permiso para crear tareas en este proyecto.')
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.project = project
            task.save()
            messages.success(request, 'Tarea creada exitosamente.')
            return redirect('project_detail', pk=project.pk)
    else:
        form = TaskForm()
        # Filtrar usuarios asignables: owner + colaboradores
        assignable_users = [project.owner] + list(project.collaborators.all())
        form.fields['assigned_to'].queryset = User.objects.filter(
            id__in=[u.id for u in assignable_users]
        )
    
    return render(request, 'tasks/task_form.html', {
        'form': form,
        'project': project,
        'action': 'Crear'
    })


# Editar tarea
@login_required
def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk)
    project = task.project
    
    # Verificar permisos
    is_owner = request.user == project.owner
    is_collaborator = request.user in project.collaborators.all()
    
    if not (is_owner or is_collaborator):
        messages.error(request, 'No tienes permiso para editar esta tarea.')
        return redirect('dashboard')
    
    # Los colaboradores solo pueden cambiar el estado
    if is_collaborator and not is_owner:
        if request.method == 'POST':
            form = TaskStatusForm(request.POST, instance=task)
            if form.is_valid():
                form.save()
                messages.success(request, 'Estado de la tarea actualizado.')
                return redirect('project_detail', pk=project.pk)
        else:
            form = TaskStatusForm(instance=task)
        
        return render(request, 'tasks/task_status_form.html', {
            'form': form,
            'task': task,
            'project': project
        })
    
    # El owner puede editar todo
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tarea actualizada exitosamente.')
            return redirect('project_detail', pk=project.pk)
    else:
        form = TaskForm(instance=task)
        assignable_users = [project.owner] + list(project.collaborators.all())
        form.fields['assigned_to'].queryset = User.objects.filter(
            id__in=[u.id for u in assignable_users]
        )
    
    return render(request, 'tasks/task_form.html', {
        'form': form,
        'project': project,
        'task': task,
        'action': 'Editar'
    })


# Eliminar tarea (solo owner)
@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    project = task.project
    
    # Solo el owner puede eliminar
    if request.user != project.owner:
        messages.error(request, 'Solo el propietario del proyecto puede eliminar tareas.')
        return redirect('project_detail', pk=project.pk)
    
    if request.method == 'POST':
        task.delete()
        messages.success(request, 'Tarea eliminada exitosamente.')
        return redirect('project_detail', pk=project.pk)
    
    return render(request, 'tasks/task_confirm_delete.html', {
        'task': task,
        'project': project
    })


# Importar User al inicio del archivo
from django.contrib.auth.models import User
