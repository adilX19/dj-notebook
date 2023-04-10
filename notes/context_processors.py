from .models import NoteType, NoteBook
from django.urls import resolve

def get_all_notes_type(request):
  context = {
    'all_note_types': NoteType.objects.all(),
    'notebook_global': request.user.notebooks.first() if request.user.is_authenticated else None
  }
  return context

def get_url_name(request):
  url_name = resolve(request.path_info).url_name
  return {'url_name': url_name}