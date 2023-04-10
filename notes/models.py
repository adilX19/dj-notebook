from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from ckeditor_uploader.fields import RichTextUploadingField
from ckeditor.fields import RichTextField
from django.utils import timezone
from django.utils.text import slugify
from accounts.models import UserAccount

class Diary(models.Model):
  user = models.OneToOneField(UserAccount, related_name='diary', on_delete=models.CASCADE)
  title = models.CharField(max_length=200)

  def __str__(self):
    return self.title

class DiaryPage(models.Model):
  diary   = models.ForeignKey(Diary, on_delete=models.CASCADE, related_name='pages')
  text    = models.TextField()
  page_no = models.PositiveIntegerField(null=True, blank=True, default=0)
  date_created = models.DateTimeField(auto_now_add=True)
  date_updated = models.DateTimeField(auto_now=True)

  def save(self, *args, **kwargs):
    if self.page_no == 0:
      self.page_no = self.diary.pages.count() + 1
    super(DiaryPage, self).save(*args, **kwargs)

class NoteType(models.Model):
	type_name = models.CharField(max_length=100)
	icon_class = models.CharField(max_length=50, null=True, blank=True)
	slug = models.SlugField(max_length=300, unique=True, null=True, blank=True)

	def save(self, *args, **kwargs):
		self.slug = slugify(self.type_name)
		super(NoteType, self).save(*args, **kwargs)

	def get_absolute_url(self):
		return f"/notes/{self.slug}/note_type/"

	def __str__(self):
		return self.type_name

class NoteBook(models.Model):
  user = models.ForeignKey(UserAccount, related_name='notebooks', on_delete=models.CASCADE)
  name = models.CharField(max_length=200)
  discription = models.TextField(null=True, blank=True)
  date_updated = models.DateTimeField(auto_now=True)
  slug = models.SlugField(max_length=300, unique=True, null=True, blank=True)

  def save(self, *args, **kwargs):
    self.slug = f"{slugify(self.name)}-{slugify(timezone.now())}"
    super(NoteBook, self).save(*args, **kwargs)

  def __str__(self):
    return self.name

class StickyNote(models.Model):
  user = models.ForeignKey(UserAccount, related_name='sticky_notes', on_delete=models.CASCADE)
  text = models.TextField()
  slug = models.SlugField(max_length=200, unique=True, null=True, blank=True)
  date_created = models.DateTimeField(auto_now_add=True)
  date_updated = models.DateTimeField(auto_now=True)

  def save(self, *args, **kwargs):
    self.slug = f"{slugify(self.user.username)}-{slugify(timezone.now())}"
    super(StickyNote, self).save(*args, **kwargs)

  def __str__(self):
    return f"Sticky Note-{self.id}"

class Note(models.Model):
  note_type    = models.ForeignKey(NoteType, related_name='notes', on_delete=models.CASCADE, blank=True)
  note_book    = models.ForeignKey(NoteBook, related_name='notes', on_delete=models.CASCADE, blank=True)
  slug         = models.SlugField(max_length=300, unique=True, null=True, blank=True)
  trashed = models.BooleanField(default=False, null=True, blank=True)
  date_created = models.DateTimeField(auto_now_add=True)
  date_updated = models.DateTimeField(auto_now=True)

  # GENERIC RELATION WITH DIFF TYPES OF NOTES
  content_type        = models.ForeignKey(ContentType, on_delete=models.CASCADE, limit_choices_to = {
      'model__in': (
        'blanknote', 'essayoutline', 'lecturenote',
        'mealplanner', 'meetingnote', 'projectplan',
        'todonote'
      )
    })
  object_id           = models.PositiveIntegerField()
  note_content_object = GenericForeignKey()
                                          
  def save(self, *args, **kwargs):
    self.slug = f"{slugify(self.note_book.name)}-{slugify(timezone.now())}"
    super(Note, self).save(*args, **kwargs)

  def __str__(self):
    return f"{self.note_type} - {self.id}"

class BaseNote(models.Model):
	title 			 = models.CharField(max_length=300) 

	class Meta:
		abstract = True

class BlankNote(BaseNote): 
	text_content = RichTextUploadingField()

	def __str__(self):
		return self.title

class TodoNote(BaseNote):
	pass

	def __str__(self):
		return self.title	

class TodoItem(models.Model): 
	todo       = models.ForeignKey(TodoNote, related_name='items', on_delete=models.CASCADE)
	item       = models.CharField(max_length=300)
	completed  = models.BooleanField(default=False)

	def __str__(self):
		return self.item

class LectureNote(BaseNote):
	course       = models.CharField(max_length=300)
	date         = models.DateTimeField(auto_now_add=True)
	professor    = models.CharField(max_length=300)
	text_content = RichTextUploadingField()
	summary			 = models.TextField(max_length=300)

	def __str__(self):
		return self.title

class MeetingNote(BaseNote):
	date_time     = models.DateTimeField(blank=True)
	goal          = models.CharField(max_length=300)
	attendees = RichTextField(config_name='simple')
	agenda = RichTextField(config_name='simple')
	notes = RichTextUploadingField()

	def __str__(self):
		return self.title

class ProjectPlan(BaseNote):
	summary 			   = models.TextField()
	major_milestones = RichTextUploadingField(config_name='moderate')

	def __str__(self):
		return self.title

class EssayOutline(BaseNote):
	introduction = RichTextField(config_name='simple')
	body 				 = RichTextField(config_name='simple')
	conclusion   = RichTextField(config_name='simple') 

	def __str__(self):
		return self.title

class MealPlanner(BaseNote):
	week = models.DateTimeField(null=True, blank=True)	

	def __str__(self):
		return self.title

class DayMeal(models.Model):
	DAYS_CHOICES = (
		('sunday', 'Sunday'),
		('monday', 'Monday'),
		('tuesday', 'Tuesday'),
		('wednesday', 'Wednesday'),
		('thursday', 'Thursday'),
		('friday', 'Friday'),
		('saturday', 'Saturday'),
	)

	mealplanner = models.ForeignKey(MealPlanner, related_name='days_instances', on_delete=models.CASCADE)
	breakfast   = models.CharField(max_length=100)
	lunch       = models.CharField(max_length=100)
	dinner      = models.CharField(max_length=100)

	def __str__(self):
		return f"Meal Plan from {self.mealplanner.week} of {self.mealplanner.title}"

class Trash(models.Model):
  note = models.ForeignKey(Note, on_delete=models.CASCADE)
  
  def __str__(self):
    return f"{self.note.note_type} from {self.note.note_book}"

class SharedNote(models.Model):
  note = models.ForeignKey(Note, on_delete=models.CASCADE)
  sender = models.ForeignKey(UserAccount, related_name='sent_notes', on_delete=models.CASCADE)
  receiver = models.ForeignKey(UserAccount, related_name='received_notes', on_delete=models.CASCADE)
  date_shared = models.DateTimeField(auto_now_add=True)

  # adil.sent_notes.all() all notes sent by adil  
  # adil.received_notes.all() all notes received by adil

  class Meta:
    verbose_name_plural = 'Shared Notes'
