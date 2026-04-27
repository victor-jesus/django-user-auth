from django import forms
from .models import Task

class CreateTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'status', 'due_at']
        widgets = {
            'due_at': forms.DateTimeInput(
                attrs={
                    'type': 'datetime-local',
                    'class': 'form-control',
                },
                format='%d-%m-%YT%H:%M'
            ),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'form-control'
            })
            
class TaskEditForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'status', 'due_at']
        widgets = {
            'due_at': forms.DateTimeInput(
                attrs={'type': 'datetime-local'},
                format='%Y-%m-%dT%H:%M',
            ),
        }
        
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            # Remove o formato UTC que o Django coloca por padrão no datetime
            self.fields['due_at'].input_formats = ['%Y-%m-%dT%H:%M']