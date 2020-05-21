from django.db import models
from django.contrib.auth.models import User

class Register(models.Model):
	user = models.OneToOneField(User,on_delete=models.CASCADE)
	mobile_name = models.IntegerField()

	def __str__(self):
		return self.user.username


class ImageModel(models.Model):
	user  = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
	images = models.ImageField(upload_to='profiles',null=True,blank=True)


