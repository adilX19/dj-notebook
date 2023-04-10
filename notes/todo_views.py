from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import TodoNote ,TodoItem

def add_item_to_list_view(request, todo_id):
  todo = get_object_or_404(TodoNote, id=int(todo_id))
  if request.method == 'POST' and request.user.is_authenticated:
    new_item = TodoItem(todo=todo, item=request.POST['item'])
    new_item.save()
    return JsonResponse({
      'id': new_item.id,
      'item': new_item.item,
      'completed': new_item.completed
    })
  return JsonResponse({}, status=403) # Forbidden 

def mark_item_as_complete_view(request, item_id):
  item = get_object_or_404(TodoItem, id=item_id)
  item.completed = True
  item.save()
  return JsonResponse({'message': 'Marked Success'}, status=200)

def delete_completed_items_view(request, todo_id):
  todo = get_object_or_404(TodoNote, id=todo_id)
  [todo_item.delete() for todo_item in todo.items.all() if todo_item.completed] 
  return JsonResponse({}, status=200)

def delete_all_items_view(request, todo_id):
  todo = get_object_or_404(TodoNote, id=todo_id)
  [todo_item.delete() for todo_item in todo.items.all()]
  return JsonResponse({}, status=200)

