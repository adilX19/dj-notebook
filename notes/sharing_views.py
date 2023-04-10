from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Note, SharedNote
from easy_pdf.rendering import render_to_pdf
from django.core.mail import EmailMessage
from django.conf import settings

@login_required(login_url='/accounts/login/')
def shared_note_open_view(request, note_slug):
  note = Note.objects.get(slug=note_slug)
  template_name = 'notes/shared_notes_details.html'
  included_note_template = f"notes/note_type_templates/{note.content_type.model}.html"
  context = {
    'note': note,
    'included_note_template': included_note_template
  }
  return render(request, template_name, context)

def save_shared_note_view(request, note_slug):
  if request.user.is_authenticated:
    note = Note.objects.get(slug=note_slug)
    received_notes = request.user.received_notes.all()

    if received_notes.filter(note=note).exists():
      return JsonResponse({
        'message': 'You already saved this note..',
        'alert_class': 'alert-info'
      })
    
    SharedNote.objects.create(
      note=note,
      sender=note.note_book.user,
      receiver=request.user
    )
    return JsonResponse({
      'message': 'Note has been saved Successfully',
      'alert_class': 'alert-success'
    })
  return JsonResponse({
    'message': 'Something went wrong',
    'alert_class': 'alert-danger'
  })

def shared_notes_list_view(request, note_slug=None):
  shared_objects = request.user.received_notes.order_by('-date_shared')
  current_note = None

  if shared_objects:
    current_note = shared_objects.get(note__slug=note_slug).note if note_slug else shared_objects.last().note
    
  template_name = 'notes/shared_notes_list.html'
  context = {
    'shared_objects': shared_objects,
    'current_note': current_note,
    'current_note_template':  f"notes/note_type_templates/{current_note.content_type.model}.html" if current_note else None
  }
  return render(request, template_name, context)

def send_note_document_email_view(request, note_slug):
  if request.user.is_authenticated and request.method == 'POST':
    note = Note.objects.get(slug=note_slug, note_book__user=request.user)
    
    # generating pdf response
    model_name = note.note_type.slug.replace('-', '')
    template_src_path = f'notes/note_type_templates/{model_name}.html'
    context_data = {'current_note': note}

    pdf = render_to_pdf(template_src_path, context_data)

    # sending this pdf via email

    # setting  credentials for sending user
    settings.EMAIL_HOST_USER = request.POST['sender_email']
    settings.EMAIL_HOST_PASSWORD = request.POST['sender_password']

    email_msg = EmailMessage(
      subject=request.POST['subject'],
      body=request.POST['message'],
      from_email=request.POST['sender_email'],
      to=[request.POST['to_email']]
    )

    email_msg.attach(
      f'{note.note_content_object.title}.pdf',
      pdf, 'application/pdf' 
    )

    try:
      email_msg.send()
      print('EMAIL SENT SUCCESSFULLY...')
    except:
      print('EMAIL SENDING FAILED...')
    
    return redirect('notes:dashboard')
  return JsonResponse({}, status=403)