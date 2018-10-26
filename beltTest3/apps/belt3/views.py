from django.shortcuts import render, redirect
from . models import *
from django.contrib import messages
import bcrypt

def index(request):
	return render(request, 'belt3/index.html')

def register(request):
	errors = User.objects.registrationValidation(request.POST)
	if len(errors) == 0:
		hashpw= bcrypt.hashpw(request.POST['password'].encode(),
			bcrypt.gensalt()).decode()
		user= User.objects.create(
			firstName = request.POST['firstName'],
			lastName = request.POST['lastName'],
			email = request.POST['email'],
			password = hashpw,
			)
		request.session['id'] = user.id
		print("*"*60, "register",
			request.session['id'],
			"*"*60
			)
		return redirect("/travels/" + str(user.id))
	else:
		for e in errors:
			messages.error(request, e)
		return redirect("/")

def login(request):
	errors = User.objects.loginValidation(request.POST)
	if len(errors) == 0:
		user = User.objects.filter(email=request.POST['email'])
		request.session['id'] = user[0].id
		print("*"*60,
			"login",
			request.session['id'],
			"*"*60
			)
		return redirect("/travels/" + str(request.session['id']))
	else:
		for e in errors:
			messages.error(request, e)
		return redirect("/")

def travels(request, user_id):
	print("*"*60,
		"Travels",
		"*"*60
		)
	context = {
		"user": User.objects.get(id= request.session['id']),
		"Utrips": User.objects.get(id= request.session['id']).trips.all(),
		"others": User.objects.get(id= request.session['id']).joiner.all(),
		"Atrips": Trip.objects.all()
	}
	return render(request, "belt3/travels.html", context)

def logout(request):
	null = request.session['id']
	return redirect("/")

def createplan(request):
	errors= Trip.objects.TripVal(request.POST)
	if len(errors) == 0:
		Trip.objects.create(
			dest= request.POST['dest'],
			desc= request.POST['desc'],
			start= request.POST['start'],
			end= request.POST['end'],
			planner= User.objects.get(id= request.session['id'])
			)
		return redirect('/travels/' + str(request.session['id']))
	else:
		for e in errors:
			messages.error(request, e)
		return redirect("/addtrip")


	#
	#
	# else:
	#     for message in newplan[1]:
	#         messages.error(request, message)
	#     return redirect('/addtrip')

def addtrip(request):
	return render(request, 'belt3/addtrip.html')

def viewtrip(request, trip_id):
	context = {
		"trip": Trip.objects.get(id= trip_id),
		"others": Trip.objects.get(id= trip_id).join.all()
	}
	print("*"*60,
		trip_id,
		"*"*60
		)
	return render(request, 'belt3/view.html', context)

def delete(request, trip_id):
	Trip.objects.get(id= trip_id).delete()
	return redirect("/travels/" + str(request.session['id']))

def cancel(request, trip_id):
	joiner= User.objects.get(id= request.session['id'])
	trip= Trip.objects.get(id=trip_id)
	trip.join.remove(joiner)
	return redirect("/travels/" + str(request.session['id']))

def join(request, trip_id):
	joiner= User.objects.get(id= request.session['id'])
	trip= Trip.objects.get(id=trip_id)
	trip.join.add(joiner)
	return redirect("/travels/" + str(request.session['id']))
