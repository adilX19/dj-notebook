from django.shortcuts import render, redirect, get_object_or_404
from .utils import *
from .models import *
from .forms import MealPlannerDaysFormSet, NotebookForm
from django.http import JsonResponse, HttpResponse
from django.db.models import Q
from random import randint
from datetime import datetime

def site_home_view(request):
  template_name = 'notes/site/home.html'
  return render(request, template_name, {})

def site_about_view(request):
  template_name = 'notes/site/about.html'
  return render(request, template_name, {})

def site_features_view(request):
  template_name = 'notes/site/features.html'
  return render(request, template_name, {})    

def dashboard_home_view(request):
  template_name = 'notes/dashboard_home.html'
  context = {
    'recent_notes': Note.objects.filter(trashed=False).order_by('-date_updated')[:6],
    'sticky_notes': request.user.sticky_notes.all(),
    'greeting_message': time_greeting_message(datetime.now().hour),
    'weather_details': get_weather_updates('Dera Ismail Khan'),
    'day': datetime.now().strftime("%a"),
    'today': datetime.now().date(),
  }
  return render(request, template_name, context)

def notes_list_view(request, note_slug=None, notebook_slug=None):
  # ======================================================
	# | FOLLOWING POSSIBE REQUESTS CAN BE MADE TO THIS VIEW
	# ======================================================
	# | 1 - dispay 1st note from all notes (both None param)
	# | 2 - display specific note from all notes
	# | 3 - display 1st note from specific notebook
	# | 4 - display specific note from specific notebook
	# =======================================================

  notebook = NoteBook.objects.get(slug=notebook_slug) if notebook_slug else None
  notes = notebook.notes.filter(trashed=False) if notebook else Note.objects.filter(note_book__user=request.user, trashed=False)
  current_note = notes.last() if not note_slug else notes.get(slug=note_slug)
  
  context = {
    'notebook': notebook,
    'notes': notes.order_by('-date_created'),
    'current_note': current_note, 
    'current_note_template_name': f"notes/note_type_templates/{current_note.content_type.model}.html" if current_note else None
  }

  rendered_template_name = 'notes/notes_list.html'
  return render(request, rendered_template_name, context)

def notebook_display_view(request, notebook_slug=None):
  # 1 first notebook from all notebooks (slug=None)
  # 2 specific notebook from all notebooks(slug=given)

  notebooks = NoteBook.objects.filter(user=request.user)
  current_notebook = notebooks.get(slug=notebook_slug) if notebook_slug else notebooks.first()

  template_name = 'notes/notebook_list.html'
  context = {
		'current_notebook': current_notebook,
		'notebooks': notebooks
	}
  return render(request, template_name, context)

# /notes/<notetype_slug>/<notebook_id>/create => for creation
# /notes/<notetype_slug>/<notebook_id>/<lecturenote_id>/update => for updation

def notebook_create_update_view(request, notebook_slug=None):
  obj = NoteBook.objects.get(user=request.user, slug=notebook_slug) if notebook_slug else None
  form = NotebookForm(request.POST or None, instance=obj)

  if request.method == 'POST' and not request.is_ajax():
    if form.is_valid():
      notebook = form.save(commit=False)
      notebook.user = request.user
      notebook.save()
      return redirect('notes:display_notebooks')

  template_name = 'notes/notebook_modal_form.html'    
  context = {
    'object': obj,
    'form': form
  }
  return render(request, template_name, context)

def delete_notebook_view(request, notebook_slug):
  notebook = get_object_or_404(NoteBook, slug=notebook_slug)
  if request.user.is_authenticated and notebook.user == request.user:
    notebook.delete()
    return redirect('notes:display_notebooks')

def note_create_update_view(request, note_type_slug, notebook_id, id=None):
  note_book  = get_object_or_404(NoteBook, id=notebook_id, user=request.user)
  note_type  = get_object_or_404(NoteType, slug=note_type_slug)
  model_name = note_type_slug.replace('-', "")

  # pointed => (LectureNote, MeetingNote, MealPlanner etc)  1st created
  # pointing => Note                    2nd created and linked with 1st
  
  model = get_content_model(model_name) # going to extract model_instance
  obj   = get_object_or_404(model, id=id) if id else None # check if created or updated ??
  form  = get_content_modelform(model, instance=obj) # extract model_form for the model and provide instance if user is going to update the already existing model. In case if no obj is given, instance will be none and form will be empty.

  formset = MealPlannerDaysFormSet(instance=obj, data=None) if model_name == 'mealplanner' else None 

  if request.method == 'POST':

    form = get_content_modelform(model, instance=obj, data=request.POST, files=request.FILES)

    # MealPlanner - (7 MealDays) -> Note

    if model_name == 'mealplanner':
      # 1st MealPlanner saved
      # 2nd MealDays formset saved and attached to MealPlanner
      # 3rd MealPlanner linked with Note
      content_object = validate_and_save_note_object(form) # 1st
      formset = MealPlannerDaysFormSet(instance=obj, data=request.POST) # 2nd
      saved = validate_and_save_note_related_mealplanner_object(formset,  note_type, note_book, content_object, id) # 2nd + 3rd 
      if saved:	return redirect('notes:first_note_from_specific_notebook', note_book.slug)
    else:
      content_object = validate_and_save_note_object(form) # pointed object
      if not id:  create_new_content_object(note_type, note_book, content_object) # creating pointing object if no id is given
      return redirect('notes:first_note_from_specific_notebook', note_book.slug)

  note_form_template = f"notes/note_type_forms/{model_name}_form.html"
  rendered_template_name = 'notes/note_form.html'

  context = {
    'form': form,  
    'formset': formset,
    'note_form_template':note_form_template,
    'current_object': obj,
    'notes': note_book.notes.filter(trashed=False),
    'notebook': note_book
  }
  return render(request, rendered_template_name, context)


def create_update_stickynotes_view(request):
  if request.method == 'POST':
    note_text = request.POST['note_text']
    slug = request.POST['slug']

    if slug:
      sticky_note = StickyNote.objects.get(user=request.user, slug=slug)
      sticky_note.text = note_text
      sticky_note.save()
      response = {
        'message': 'Note updated successfully',
        'slug': sticky_note.slug
      }
    else:
      new_sticky_note = StickyNote(user=request.user, text=note_text)  
      new_sticky_note.save()
      response = {
        'message': 'Note created successfully',
        'slug': new_sticky_note.slug
      }
    return JsonResponse(response, status=200)
  return JsonResponse({}, status=403)  


def stickynote_delete_view(request, stickynote_slug=None):
  if stickynote_slug == 'null':
    return JsonResponse({}, status=200)

  sticky_note = get_object_or_404(StickyNote, slug=stickynote_slug)  
  if sticky_note.user == request.user:
    sticky_note.delete()
    return JsonResponse({}, status=200)
  return JsonResponse({}, status=403) # Forbidden 

def export_to_pdf_view(request, note_slug):
	note = get_object_or_404(Note, slug=note_slug, trashed=False)
	model_name = note.note_type.slug.replace('-', "")
	template_src_path = f'notes/note_type_templates/{model_name}.html'
	context_data = {'current_note': note}

	pdf = render_to_pdf(template_src_path, context_data)

	if pdf:
		response = HttpResponse(pdf, content_type='application/pdf')
		filename = f'{model_name}_{timezone.now()}.pdf'
		content = f"inline; filename={filename}"
		download = request.GET.get('download')
		if download:
			content = f"attachment; filename={filename}"
		response['Content-Disposition'] = content
		return response
	return HttpResponse("Not found")

def search_note_view(request):
  if 'query' in request.GET:
    query = request.GET.get('query').upper()
    results = []

    for note in Note.objects.filter(trashed=False, note_book__user=request.user):
      title =  note.note_content_object.title.upper()

      if (title.startswith(query)) or (query in title):
        item = {
          'note_id':note.id,
          'title': note.note_content_object.title,
          'note_slug': note.slug,
          'notebook_slug': note.note_book.slug
        }
        results.append(item)
      
      if query and len(results) > 0:
        response = {'search_results': results}
      else:
        response = {'search_results': 'No results found'}

    return JsonResponse(response)
  return JsonResponse({}, status=400)


# /notes/<slug>/export/pdf/
"""
In a regular HTTP response, the Content-Disposition response header is a header indicating if the content is expected to be displayed inline in the browser, that is, as a Web page or as part of a Web page, or as an attachment, that is downloaded and saved locally.
"""


# TRASH VIEWS
# 1 - can view trash items
# 2 - can add an item to trash
# 3 - can restore an item from trash
# 4 - can empty the trash
def trash_items_list_view(request):
  trashed_notes = [trashed_note.note for trashed_note in Trash.objects.all()]

  template_name = 'notes/trash.html'
  context = {'trashed_notes': trashed_notes}
  return render(request, template_name, context)

def move_to_trash_view(request, note_slug):
  note = get_object_or_404(Note, slug=note_slug, trashed=False, note_book__user=request.user) # false isleye k wo trash ka hissa na ho pehly sy

  if not Trash.objects.filter(note=note).exists():
    # agr trash mein ni hai to trash mein dalo
    Trash.objects.create(note=note) # new row containing note-link
    note.trashed = True
    note.save()
    return redirect('notes:first_note_from_specific_notebook', note.note_book.slug)

def restore_from_trash_view(request, note_slug):
  note = get_object_or_404(Note, slug=note_slug, trashed=True, note_book__user=request.user) # true isleye k wo trash ka hissa hona chahye

  if Trash.objects.filter(note=note).exists():
    # agr trash mein hai to nikalo
    Trash.objects.get(note=note).delete()
    note.trashed = False
    note.save()
    return redirect('notes:first_note_from_specific_notebook', note.note_book.slug)

def empty_notes_trash_view(request):
  trashed_notes = [trashed_note.note for trashed_note in Trash.objects.all()]

  for trashed_note in trashed_notes:
    trashed_note.note_content_object.delete() # Actual Note deleted
    trashed_note.delete()                     # Its reference is also deleted 
  return redirect('notes:first_note_from_all_notes')

