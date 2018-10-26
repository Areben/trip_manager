from django.db import models
import bcrypt, re
from datetime import date, datetime
from time import strptime
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
	def registrationValidation(self, input):
		errors = []
		if len(input['firstName'])<3:
			errors.append("First name should be at least 3 letters")
		if len(input['lastName'])<3:
			errors.append("Last Name should be at least 3 letters")
		if len(input['password'])<8:
			errors.append("Password should be at least 8 letters")
		if not EMAIL_REGEX.match(input['email']):
			errors.append("Invalid Email format")
		if input['password'] != input['confirmPassword']:
			errors.append("Password's do not match")
		return errors

	def loginValidation(self, input):
		errors = []
		user = User.objects.filter(email = input['email'])
		if len(user) == 0:
			errors.append("Email or Password is incorrect")
			return errors
		if bcrypt.checkpw(input['password'].encode(), user[0].password.encode()):
			print("Passwords match!")
		else:
			errors.append("Passwords do not match")
		return errors

class TripManager(models.Manager):
	def TripVal(self, input):
		errors = []
		if len(input["dest"])<2:
			errors.append("At least 3 characters needed to make a Trip.")
		if len(input["desc"])<2:
			errors.append("At least 3 characters needed for a Trip Description.")
		if str(date.today()) > str(input['start']):
			errors.append("Please input a valid Date. Note: Start time can not be in the past.")
		if str(date.today()) > input['end']:
			errors.append("Please input a valid Date. Note: End date must be in the future")
		if input['start'] > input['end']:
			errors.append("Travel Date From can not be in the future of Travel Date To")
		return errors

class User(models.Model):
	firstName = models.CharField(max_length=20)
	lastName = models.CharField(max_length=20)
	email = models.EmailField()
	password = models.CharField(max_length=20)
	createdAt = models.DateTimeField(auto_now_add=True)
	updatedAt = models.DateTimeField(auto_now=True)
	objects = UserManager()

class Trip(models.Model):
	dest = models.CharField(max_length= 25)
	desc = models.CharField(max_length= 25)
	start = models.DateField()
	end = models.DateField()
	attending = models.BooleanField(default= True)
	join = models.ManyToManyField(User, related_name= "joiner")
	planner = models.ForeignKey(User, related_name= "trips", on_delete= models.CASCADE)
	createdAt = models.DateTimeField(auto_now_add= True)
	updatedAt = models.DateTimeField(auto_now= True)
	objects = TripManager()
