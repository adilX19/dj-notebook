from django.apps import apps
from django.forms.models import modelform_factory
from django.http import HttpResponse, request
from django.template.loader import get_template
from io import BytesIO
from xhtml2pdf import pisa
from .models import Note
import requests
from django.conf import settings

def get_content_model(model_name): #lecturenote
  """returns model for the specific contenttype, otherwise none"""
  selected_models = (
		'blanknote', 'essayoutline', 'lecturenote',
		'mealplanner', 'meetingnote', 'projectplan',
		'todonote'
	)
  if model_name in selected_models:
    return apps.get_model(app_label='notes', model_name=model_name)
  return None

def get_content_modelform(model, *args, **kwargs):
  """returns modelform for the provided model"""
  Form = modelform_factory(model, exclude=['date_created', 'date_updated'])
  return Form(*args, **kwargs)

def validate_and_save_note_object(form):
  # pointed object (LectureNote, BlankNote etc)
  if form.is_valid():
    content_object = form.save(commit=False) # I want this, so give me
    content_object.save() # Now I have this, you can save this
    return content_object
  return None

def create_new_content_object(note_type, note_book, content_object): 
  # Pointing object creation
  Note.objects.create(note_type=note_type, note_book=note_book, note_content_object=content_object)
  return None
  
  # MealPlanner -> DayMeals7 -> Note
def validate_and_save_note_related_mealplanner_object(formset, note_type, note_book, content_object, id):
  if formset.is_valid():
    formset.instance = content_object
    formset.save()
    # 3rd step
    if not id:	create_new_content_object(note_type, note_book, content_object)
    return True
  return False
  
def render_to_pdf(template_src_path, context_data={}):
	template = get_template(template_src_path)
	html = template.render(context_data)
	result = BytesIO()
	try:
		pdf = pisa.pisaDocument(BytesIO(html.encode("utf-8")), result)
	except:
		pdf = None

	if not pdf.err:
		return HttpResponse(result.getvalue(), content_type='application/pdf')
	return None 

def reorder_page_numbers(diary):
  pages = diary.pages.all()
  page_nos = range(1, pages.count()+1)

  for page, new_page_no in zip(pages, page_nos):
    page.page_no = new_page_no
    page.save()

def time_greeting_message(hour):
  message = ""
  if hour < 12 and hour >= 1:
    message = "Good Morning"
  elif hour >= 12 and hour <= 16:
    message = "Good Afternoon"
  elif hour >= 17 and hour <= 20:
    message  = "Good Evening"
  else:
    message = "Good Night"
  return message

def get_weather_updates(city):
  url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid={}'
  city_weather = requests.get(url.format(city, settings.OPEN_WEATHER_API_KEY)).json()

  response = {
    'city': city,
    'temperature': city_weather['main']['temp'],
    'description': city_weather['weather'][0]['description'],
    'icon': city_weather['weather'][0]['icon']
  }
  return response
