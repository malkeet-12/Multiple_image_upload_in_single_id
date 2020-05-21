from django.shortcuts import render
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from rest_framework.views import APIView
from django.http import JsonResponse
from . models import *
from django.contrib.auth import authenticate, login
from django.core.files.storage import FileSystemStorage
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import viewsets, status
# Create your views here.
class Registers(APIView):
	def post(self,request):
		try:
			username = request.POST.get('username')
			print(username)
			email = request.POST.get('email')
			print(email)
			password = request.POST.get("password")
			print(password)
			mobile_number = request.data.get('mobile_number')
			print(mobile_number)

			user = User.objects.create_user(username=username,email=email,password=password)
			if user:
				token = Token.objects.create(user=user)
			custom_user = Register.objects.create(user=user,mobile_name=mobile_number)
			content = {
				'message': 'Registration is successfully done',
				'token':token.key
			}
			return JsonResponse(content,safe=False)
		except Exception as e:
			print(e)



class LoginView(APIView):
	def post(self,request):
		try:
			username = request.POST.get('username')
			print(username)
			password = request.POST.get('password')
			print(password)
			user = authenticate(request, username=username, password=password)
			if user:
				token, status = Token.objects.get_or_create(user = user)
				login(request, user)
				if request.FILES:
					for count, image_name in enumerate(request.FILES.getlist("image")):
						fs = FileSystemStorage()
						filename = fs.save(image_name.name, image_name)
						filename = fs.url(filename)
						print('yesyesyes')
						ImageModel.objects.create(user=user,images=filename)
						print('yesyesyes1')
					all_obj=ImageModel.objects.filter(user=user)
					images_list=[]
					for i in all_obj:
						dic={}
						dic['image'] = i.images.name
						images_list.append(dic)
					content = {
						'id':user.id,
						'title':'This is task title',
						'user':user.username,
						'images':images_list
					}
				else:
					content = {
					'message': 'login successfully',
					'token': token.key
					}
				return JsonResponse(content,safe=False) 
			else:
				content = {
					'message': 'Wrong Credentials'
				}
				return JsonResponse(content,safe=False)
		except Exception as e:
			print(e)



class LogoutView(APIView):
	permission_classes = (IsAuthenticated,)
	authentication_class =TokenAuthentication
	def get(self, request, format=None):
		request.user.auth_token.delete()
		return Response(status=status.HTTP_200_OK)


class ChangePassword(APIView):
	permission_classes = (IsAuthenticated,)
	authentication_class = TokenAuthentication
	def post(self,request,*args,**kwargs):
		try:
			print(request.user.id)
			current_password = request.POST['curr_pass']
			print(current_password)
			user = User.objects.get(id=request.user.id)
			print(user)
			check_pass = user.check_password(current_password)
			print(check_pass)
			if check_pass == True:
				new_password = request.POST['new_pass']
				confirm_password = request.POST['confirm_pass']
				if new_password == confirm_password:
					user.set_password(new_password)
					user.save()
					context = {
					'message': 'Your password is successfully changed'
					}
					return JsonResponse(context,safe=False)
				else:
					raise ValueError('password did not match')
			else:
				raise ValueError('user could not be found')

		except Exception as e:
			print(e)