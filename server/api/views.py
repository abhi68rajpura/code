from django.shortcuts import render
from django.http import HttpResponse
import os
import json
import csv
from datetime import datetime
import requests
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout

def index(request):
	resp=json.dumps({'msg':'ok'})
	return HttpResponse(resp,content_type="application/json")

@csrf_exempt
def createUser(request):
	
	jsn=json.loads(request.body)
	username=jsn['username']
	password=jsn['password']
	email=jsn['email']
	try:
		u = User.objects.get(username = username)
		u.delete()
	except:
		pass
	user = User.objects.create_user(username, email, password)
	resp=json.dumps({'success':True})
	return HttpResponse(resp,content_type="application/json")
	
def doLogout(request):
	logout(request)
	resp=json.dumps({'msg':'ok'});
	return HttpResponse(resp,content_type="application/json")
	
	
@csrf_exempt 
def doLogin(request):
	try:
		jsn=json.loads(request.body)
		user = authenticate(username=jsn['username'], password=jsn['password'])
		
		if user is not None:
			resp=json.dumps({'msg':'ok'});
			login(request, user)
		else:
			resp=json.dumps({'msg':'sorry'});
	except:
		resp=json.dumps({'msg':'sorry'});
		
	return HttpResponse(resp,content_type="application/json")
	
def checkLogin(request):
	if request.user.is_authenticated:
		resp=json.dumps({"msg":'ok'});
	else:
		resp=json.dumps({"msg":"sorry"})
	return HttpResponse(resp,content_type="application/json")

def getAllData(request):
	dt={}
	with open('../bin/data.json') as dt:
		dt=json.load(dt)
		
	resp=json.dumps(dt)
	return HttpResponse(resp,content_type="application/json")
	
def getDiff(request):
	diff={}
	with open('../bin/diff.json') as diff:
		diff=json.load(diff)
		
	resp=json.dumps(diff)
	return HttpResponse(resp,content_type="application/json")
	
	
def getSettings(request):
	set={}
	with open('../bin/settings.json') as set:
		set=json.load(set)
		
	resp=json.dumps(set)
	return HttpResponse(resp,content_type="application/json")
	
@csrf_exempt 
def postSettings(request):
	set=json.loads(request.body)
	with open('../bin/settings.json','w') as setw:
		setw.write(json.dumps(set))

