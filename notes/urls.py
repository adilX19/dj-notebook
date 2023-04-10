from django.urls import path
from . import views, todo_views, diary_views, sharing_views

app_name = 'notes'

urlpatterns = [

  path(
    'home/',
    views.site_home_view,
    name='site_home'
  ),

  path(
    'about/',
    views.site_about_view,
    name='site_about'
  ),

  path(
    'features/',
    views.site_features_view,
    name='site_features' 
  ),

  path(
    'dashboard/', 
    views.dashboard_home_view, 
    name='dashboard'
  ),

  path(
		'list/', 
		views.notes_list_view, 
		name='first_note_from_all_notes'
	),

	path(
		'list/<slug:note_slug>/note/', 
		views.notes_list_view, 
		name='specific_note_from_all_notes'
	),

	path(
		'list/<slug:notebook_slug>/notebook/', 
		views.notes_list_view, 
		name='first_note_from_specific_notebook'
	),

	path(
		'list/<slug:note_slug>/<slug:notebook_slug>/', 
		views.notes_list_view, 
		name='specific_note_from_sepecific_notebook'
	),

  path(
		'<slug:note_type_slug>/<int:notebook_id>/create/', 
		views.note_create_update_view, 
		name='notes_create'
	),

  path(
    'sticky/note/', 
    views.create_update_stickynotes_view, 
    name=' create_update_stickynote'
  ),

  path(
    'stickynotes/<slug:stickynote_slug>/delete/', 
    views.stickynote_delete_view, 
    name='delete_stickynote'
  ),

	path(
		'<slug:note_type_slug>/<int:notebook_id>/<int:id>/update/', 
		views.note_create_update_view, 
		name='notes_update'
	),

  path(
    'notebooks/', 
    views.notebook_display_view, 
    name='display_notebooks'
  ),

  path(
    'notebooks/<slug:notebook_slug>/', 
    views.notebook_display_view, 
    name='display_specific_notebook'
  ),

  path(
    'notebook/create/', 
    views.notebook_create_update_view, 
    name='create_notebook'
  ),

  path(
    'notebook/<slug:notebook_slug>/update/', 
    views.notebook_create_update_view, 
    name='update_notebook'
  ),

  path(
    'notebook/<slug:notebook_slug>/delete/', 
    views.delete_notebook_view, 
    name='delete_notebook'
  ),

  path(
    'export/<slug:note_slug>/pdf/', 
    views.export_to_pdf_view, 
    name='export_to_pdf'
  ),

  path(
    'search/note/', 
    views.search_note_view, 
    name='note_search'
  ),

  path(
		'trash/items/', 
		views.trash_items_list_view, 
		name='trashed_items'
	),

	path(
		'trash/empty/',
		views.empty_notes_trash_view,
		name='empty_trash'
	),

	path(
		'move/<slug:note_slug>/to-trash/', 
		views.move_to_trash_view, 
		name='move_to_trash'
	),

	path(
		'restore/<slug:note_slug>/from-trash/', 
		views.restore_from_trash_view, 
		name='restore_from_trash'
	),
]

urlpatterns += [
  path(
    'todos/<int:todo_id>/additem/', 
    todo_views.add_item_to_list_view, 
    name='add_new_item'
    ),

  path(
    'todos/items/<int:item_id>/complete/', 
    todo_views.mark_item_as_complete_view, 
    name='mark_complete'
    ),

  path(
    'todos/<int:todo_id>/delete/completed/', 
    todo_views.delete_completed_items_view, 
    name='delete_completed'
    ),

  path(
    'todos/<int:todo_id>/delete/all/', 
    todo_views.delete_all_items_view, 
    name='delete_all'
  ),
]

urlpatterns += [
  path(
    'diary/',
    diary_views.diary_pages_list_view,
    name='open_diary'
  ),

  path(
    'diary/page/<int:page_id>/',
    diary_views.diary_pages_list_view,
    name='open_diary_by_page'
  ),

  path(
    'diary/create/page/',
    diary_views.create_new_page_view, 
    name='create_page'
  ),

  path(
    'diary/page/<int:page_id>/update/',
    diary_views.update_page_view,
    name='update_page'
  ),

  path(
    'diary/page/<int:page_id>/delete/',
    diary_views.delete_page_view,
    name='delete_page'
  ),
]

# shared notes patterns 
urlpatterns += [
	path(
		'shared/',
		sharing_views.shared_notes_list_view,
		name='first_note_from_shared_notes'
	),
	path(
		'shared/<slug:note_slug>/details/',
		sharing_views.shared_notes_list_view,
		name='specific_note_from_shared_notes'
	),
	path(
		'shared/<slug:note_slug>/note/',
		sharing_views.shared_note_open_view,
		name='open_shared_note'
	),
	path('shared/<slug:note_slug>/save/note/',
    sharing_views.save_shared_note_view,
		name='save_shared_note'
	),

  path(
    'send/<slug:note_slug>/email/',
    sharing_views.send_note_document_email_view,
    name='send_note_document_mail'
  ),
]


