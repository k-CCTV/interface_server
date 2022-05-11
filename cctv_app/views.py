from time import timezone
from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404
from .models import *
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

def index(request):
      print("index 시작--------------")
      boards = {'boards': Board.objects.all()}
      return render(request, 'list.html', boards)

def post(request):
    print("post 시작--------------")
    if request.method == "POST":
        board = Board()
        board.author = request.POST['author']
        board.title = request.POST['title']
        board.content = request.POST['content']
        board.image = request.FILES.get('image')
        if board.image == None:
             raise Http404("이미지 넣어야 함!")
        board.save()
        return HttpResponseRedirect(reverse('index'))
    else:
        return render(request, 'post.html')

def detail(request, id):
    print("detail 시작--------------")
    try:
        board = Board.objects.get(pk=id)
    except Board.DoesNotExist:
        raise Http404("Does not exist!")
    return render(request, 'detail.html', {'board': board})

def edit(request, id):
      print("edit 시작--------------")
      board = Board.objects.get(pk=id)
      if  request.method == "POST":
            board.author = request.POST['author']
            board.title = request.POST['title']
            board.content = request.POST['content']
            board.image = request.FILES.get('image')
            if board.image == None:
                 raise Http404("이미지 넣어야 함!")
            board.save()
            return HttpResponseRedirect(reverse('index'))
      else:
        return render(request, 'edit.html')
  
@csrf_exempt
def delete(request,id):
      print("delete 시작--------------")
      try:
            board = Board.objects.get(pk=id)
            board.delete()
            return HttpResponseRedirect(reverse('index'))
      except:
            raise Http404("Does not exist!")
            
      