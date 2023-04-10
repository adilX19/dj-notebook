from django.db import models
from django.contrib.auth.models import AbstractUser

class UserAccount(AbstractUser):
	bio   = models.TextField(null=True, blank=True)
	image = models.FileField(upload_to='profile_images', null=True, blank=True)
	dob   = models.CharField(max_length=200, default="n/a", null=True, blank=True)
	github = models.URLField(default="n/a")
	linkedin = models.URLField(default="n/a")
	twitter = models.URLField(default="n/a")
	instagram = models.URLField(default="n/a")
	is_pr = models.BooleanField(default=False)

	@property
	def full_name(self):
		return f"{self.first_name} {self.last_name}"

	def __str__(self):
		return self.username