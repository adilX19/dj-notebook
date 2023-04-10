from django.forms.models import inlineformset_factory
from django import forms
from .models import MealPlanner, DayMeal, NoteBook

MealPlannerDaysFormSet = inlineformset_factory(
    MealPlanner, DayMeal,
    fields=['breakfast', 'lunch', 'dinner'],
    extra=7
  )

class NotebookForm(forms.ModelForm):
  class Meta:
    model = NoteBook
    fields = ['name', 'discription']  
    widgets = {
      'name': forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Title of notebook'
      }),
      'discription': forms.Textarea(attrs={
        'class': 'form-control',
        'placeholder': 'Optional description of notebook'
      })
    }


