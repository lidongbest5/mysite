from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response
from blog.models import *
from django import forms
from django.utils import simplejson as json
import datetime

def hello(request):
	return HttpResponseRedirect("/blog/")

def pkdemo(request):
	return render_to_response('pk-demo.html')

def about(request):
	return render_to_response('about.html',{'type':'about'})

def resume(request):
        return render_to_response('resume.html',{'type':'resume'})

def saying(request):
	saying_total = Saying.objects.all().count()
	reply_total = SayingComment.objects.all().count()
	favourite_total = SayingFavourite.objects.get(id=1)
	replies = SayingComment.objects.order_by('-id')[0:10]
	return render_to_response('saying.html',{"saying_total":saying_total,"reply_total":reply_total,"favourite_total":favourite_total,"replies":replies,"type":'saying'})

def sayingCotent(request,index):
	try:
		index = int(index)
	except ValueError:
		raise Http404()
	data = Saying.objects.order_by('-id')[20*(index-1):20*index]
	for item in data:
		item.reply = SayingComment.objects.filter(SayingId = item.id).order_by('-id')
	hasMore = 'false'
	if 20*index < Saying.objects.all().count():
		hasMore = 'true'
	return HttpResponse(json.dumps({"hasMore":hasMore,"data":str(render_to_response('saying-content.html',{'data':data}))}))

def setFavourite(request):
	if request.is_ajax():
		num = request.POST.get('num')
		sayingid = request.POST.get('id')
		p = Saying.objects.get(id=sayingid)
		p.favourite = int(num)
		p.save()
		q = SayingFavourite.objects.get(id=1)
		q.num = int(q.num)+1
		q.save()
	return HttpResponse(json.dumps({"code":0,"favourite":int(num)}))

class SayingForm(forms.Form):
    SayingId = forms.IntegerField()
    name = forms.CharField(required=True)
    content = forms.CharField(required=True)

def setReply(request):
	if request.is_ajax():
		form = SayingForm(request.POST)
		if form.is_valid():
			p = SayingComment(SayingId=request.POST.get('SayingId'),name=request.POST.get('name'),content=request.POST.get('content'),date=datetime.datetime.now())
			p.save()
			reply = SayingComment.objects.get(id = p.id)
			return HttpResponse(json.dumps({"code":1,"data":str(render_to_response('saying-reply.html',{'reply':reply}))}))
		else:
			return HttpResponse(json.dumps({"code":0,"data":[{"name":"name","error":form['name'].errors},{"name":"content","error":form['content'].errors}]}))

def account(request):
	num = Account.objects.get(id = 1)
	detail = AccountDetail.objects.all().order_by('-id')
	return render_to_response('account.html',{'num': num, 'detail': detail})

class accountForm(forms.Form):
    num = forms.IntegerField()
    content = forms.CharField(required=True)
    name = forms.CharField(required=True)
    owner = forms.CharField(required=True)

def clearAccount(request):
	if request.is_ajax():
		Account.objects.filter(id=1).update(he=0,han=0,yang=0,dong=0)
		return HttpResponse(json.dumps({"code":1}))

def addAccount(request):
	if request.is_ajax():
		form = accountForm(request.POST)
		if form.is_valid():
			p = AccountDetail(name=request.POST.get('name'),content=request.POST.get('content'),num=request.POST.get('num'),date=datetime.datetime.now(),owner=request.POST.get('owner'))
			p.save()
			name = request.POST.get('name')
			num = request.POST.get('num')
			num = int(num)
			input_owner=request.POST.get('input_owner')
			input_array=request.POST.get('input_newarray')
			input_array = list(input_array)
			input_array[0] = int(input_array[0])
			input_array[2] = int(input_array[2])
			input_array[4] = int(input_array[4])
			input_array[6] = int(input_array[6])
			total = input_array[0] + input_array[2] + input_array[4] + input_array[6]
			old = Account.objects.get(id = 1)
			if input_owner == '1':
				Account.objects.filter(id=1).update(he=old.he+num/total*input_array[0]-num,han=old.han+num/total*input_array[2],yang=old.yang+num/total*input_array[4],dong=old.dong+num/total*input_array[6])
			elif input_owner == '2':
				Account.objects.filter(id=1).update(he=old.he+num/total*input_array[0],han=old.han+num/total*input_array[2]-num,yang=old.yang+num/total*input_array[4],dong=old.dong+num/total*input_array[6])
			elif input_owner == '3':
				Account.objects.filter(id=1).update(he=old.he+num/total*input_array[0],han=old.han+num/total*input_array[2],yang=old.yang+num/total*input_array[4]-num,dong=old.dong+num/total*input_array[6])
			elif input_owner == '4':
				Account.objects.filter(id=1).update(he=old.he+num/total*input_array[0],han=old.han+num/total*input_array[2],yang=old.yang+num/total*input_array[4],dong=old.dong+num/total*input_array[6]-num)
			return HttpResponse(json.dumps({"code":1}))
		else:
			return HttpResponse(json.dumps({"code":0}))

def love(request):
	return render_to_response('love/index.html')
