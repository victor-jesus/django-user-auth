from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.urls import reverse

class Task(models.Model):
    class Status(models.TextChoices):
        TODO = 'todo', _('To Do')
        DOING = 'doing', _('Doing')
        DONE = 'done', _('Done')
    title = models.CharField(_("Titulo"), max_length=150)
    description = models.TextField(_("Descrição"), blank=True)
    status = models.CharField(
        max_length=10, 
        choices=Status,
        default=Status.TODO,
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="tasks"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    due_at = models.DateTimeField(_("Prazo"), auto_now=False, auto_created=False, blank=True, null=True)
    
    def __str__(self):
        return self.title
    
    @property
    def is_overdue(self):
        if not self.due_at:
            return False
        
        return self.due_at < timezone.now()
    
    @property
    def is_today(self):
        if not self.due_at:
            return False
        return self.due_at.astimezone(timezone.get_current_timezone()).date() == timezone.localdate()
    
    @property
    def is_on_time(self):
        if not self.due_at:
            return False
        
        return self.due_at and not self.is_overdue and not self.is_today
    
    def get_delete_url(self):
        return reverse('tasks:delete', kwargs={'pk': self.pk})