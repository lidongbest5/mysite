from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response
from blog.models import Blog,Comment,Message
import datetime
from django import forms
from django.utils import simplejson as json

def showBlogDetail(request, offset):
    try:
        offset = int(offset)
    except ValueError:
        raise Http404()
    data = Blog.objects.get(id=offset)
    comments = Comment.objects.filter(blogid=offset).order_by('-id')
    blogNum = Blog.objects.all().count()
    if offset == 1:
        preBlog = ""
        nextBlog = Blog.objects.get(id=offset+1)
    elif offset == blogNum:
        preBlog = Blog.objects.get(id=offset-1)
        nextBlog = ""
    else:
        preBlog = Blog.objects.get(id=offset-1)
        nextBlog = Blog.objects.get(id=offset+1)
    return render_to_response('blog.html', {'data':data, 'archive': archiveNum(), 'preBlog':preBlog, 'nextBlog':nextBlog, 'comments':comments, 'type':'blog'})

def showBlogList(request, offset):
    try:
        offset = int(offset)
    except ValueError:
        raise Http404()
    data = Blog.objects.order_by('-id')[(offset-1)*10:offset*10]
    for item in data:
        item.content = item.content.split('<!--more-->')[0]
    totalnum = Blog.objects.all().count()
    if totalnum%10 == 0:
        totalpage = totalnum/10
    else:
        totalpage = totalnum/10 + 1
    if totalpage > 10:
        pages = range(totalpage-5,totalpage+4)
    else:
        pages = range(1,totalpage+1)
    return render_to_response('blog-list.html',{'data':data, 'total':totalpage, 'page':offset, 'pages':pages, 'pre':offset-1, 'next':offset+1, 'archive': archiveNum(), 'type':'blog'})

def showBlogFirstList(request):
    return showBlogList(request, 1)

def showBlogArchive(request,year,month):
    date_start = ''.join(year) + '-' + ''.join(month) + '-01'
    date_end = ''.join(year) + '-' + ''.join(month) + '-31'
    data = Blog.objects.filter(date__range=[date_start,date_end]).order_by('-id')
    for item in data:
        item.content = item.content.split('<!--more-->')[0]
    return render_to_response('blog-archive-list.html',{'data':data, 'archive': archiveNum(), 'type':'blog'})

def showBlogCategory(request,offset):
    data = Blog.objects.filter(category=offset).order_by('-id')
    for item in data:
        item.content = item.content.split('<!--more-->')[0]
    return render_to_response('blog-archive-list.html',{'data':data, 'archive': archiveNum(), 'type':'blog'})

def archiveNum():
    return [Blog.objects.filter(date__range=["2012-12-01","2012-12-31"]).count(),Blog.objects.filter(date__range=["2013-01-01","2013-01-31"]).count(),Blog.objects.filter(date__range=["2013-03-01","2013-03-31"]).count()]

class CommentForm(forms.Form):
    blogid = forms.IntegerField()
    name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    website = forms.URLField(required=False)
    message = forms.CharField(required=True)

def setComment(request):
    if request.is_ajax():
        form = CommentForm(request.POST)
        if form.is_valid():
            p = Comment(blogid=request.POST.get('blogid'),name=request.POST.get('name'),email=request.POST.get('email'),website=request.POST.get('website'),content=request.POST.get('message'),date=datetime.datetime.now())
            p.save()
            return HttpResponse(json.dumps({"code":1,"message":{"name":request.POST.get('name'),"message":request.POST.get('message')}}))
        else:
            return HttpResponse(json.dumps({"code":0,"message":[{"name":"name","error":form['name'].errors},{"name":"email","error":form['email'].errors},{"name":"website","error":form['website'].errors},{"name":"message","error":form['message'].errors}]}))

def search(request):
    s = request.POST.get('s')
    data = Blog.objects.filter(content__contains=s).order_by('-id')
    for item in data:
        item.content = item.content.split('<!--more-->')[0]
    return render_to_response('blog-archive-list.html',{'data':data, 'archive': archiveNum(), 's':s, 'type':'blog'})

class MessageForm(forms.Form):
    name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    message = forms.CharField(required=True)

def setMessage(request):
    if request.is_ajax():
        form = MessageForm(request.POST)
        if form.is_valid():
            p = Message(name=request.POST.get('name'),email=request.POST.get('email'),message=request.POST.get('message'))
            p.save()
            return HttpResponse(json.dumps({"code":1,"message":"Thanks for leaving message..."}))
        else:
            return HttpResponse(json.dumps({"code":0,"message":[{"name":"name","error":form['name'].errors},{"name":"email","error":form['email'].errors},{"name":"message","error":form['message'].errors}]}))
