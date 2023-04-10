from django.http import JsonResponse
from django.shortcuts import render
from .models import Diary, DiaryPage
from .utils import reorder_page_numbers

def diary_pages_list_view(request, page_id=None):
  diary = request.user.diary

  # if diary has no pages, i.e diary is fresh and empty 
  if diary.pages.count() == 0:
    page = DiaryPage(diary=diary, text="")
    page.save()
  else: # 4
    # if page_id is provided give me that page, otherwise last page
    page = diary.pages.get(id=page_id) if page_id else diary.pages.last()

  print(page)  
  template_name = 'diary/pages_list.html'
  context = {'diary': diary, 'current_page': page}
  return render(request, template_name, context)

def create_new_page_view(request):
  if request.method == 'POST' and request.user.is_authenticated:
    diary = request.user.diary
    current_page = diary.pages.get(id=request.POST['current_page_id'])

    # if current page is not the last page in the diary:
    if current_page.page_no != diary.pages.last().page_no:
      next_page = diary.pages.get(page_no=current_page.page_no + 1)
      # send redirect id of that next page
      return JsonResponse({'page_id': next_page.id}, status=200)
    
    new_page = DiaryPage(diary=diary, text='')
    new_page.save()

    return JsonResponse({'page_id': new_page.id},  status=200)
  return JsonResponse({}, status=403)

def update_page_view(request, page_id):
  if request.method == 'POST' and request.user.is_authenticated:
    if page_id and ('new_text' in request.POST):
      page = request.user.diary.pages.get(id=page_id)
      page.text = request.POST['new_text']
      page.save()
      return JsonResponse({}, status=200)  # success 
    return JsonResponse({}, status=400)   # bad requestt
  return JsonResponse({}, status=403)     # forbidden 

def delete_page_view(request, page_id):    
  if request.user.is_authenticated and  page_id:
    pages = request.user.diary.pages

    current_page = pages.get(id=page_id)
    previous_page_id = None

    if current_page.page_no > 1:
      # if there is a page behind current page
      previous_page_id = pages.get(page_no=current_page.page_no - 1).id

    current_page.delete()
    reorder_page_numbers(request.user.diary)
    return JsonResponse({'page_id': previous_page_id}, status=200)
  return JsonResponse({}, status=403)