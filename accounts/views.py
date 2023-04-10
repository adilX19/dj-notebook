from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import login, logout, authenticate
from .models import UserAccount

def login_view(request):
	if request.method == "POST":

		username = request.POST['username']
		password = request.POST['password']

		user = authenticate(username=username, password=password)

		if user is not None:
			if user.is_active:
				login(request, user)
				return redirect('blog:home_page')
			else:
				return HttpResponse("<h1>Account has been disabled...</h1>")
		else:
			return HttpResponse("<h1>No such user with such credentials...</h1>")

	template_name = 'login_form.html'
	context = {}
	return render(request, template_name, context)


def logout_view(request):
	logout(request)
	return redirect('accounts:login')

def signup_view(request):

	if request.method == 'POST':
		username = request.POST['username']
		email = request.POST['email']
		password = request.POST['password']
		conf_password = request.POST['conf_password']

		if username and email:
			user = UserAccount(username=username, email=email)
			if password == conf_password and password != "":
				user.set_password(conf_password)
				user.save()
				return redirect('accounts:login')
			else:
				return HttpResponse("<h1>Password's didn't matched...</h1>")

	template_name = 'signup_form.html'
	context = {}
	return render(request, template_name, context)


# USERNAME VALIDATION VIEW FOR AJAX-REQUEST...
def check_username_validity(request, username):
	if UserAccount.objects.filter(username=username).exists():
		return JsonResponse({'used': True })
	else:
		return JsonResponse({'used': False })