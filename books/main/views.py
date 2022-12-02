from django.shortcuts import redirect
from django.http import HttpResponse
from django.shortcuts import render
from django.db.models import Q
from faker import Faker
import random

from .models import Book
from .forms import BookForm


def new_book(request):
    n = request.GET.get('numbers')
    fake = Faker()
    for i in range(int(n)):
        a = fake.name()
        ttl = fake.sentences(1)[0]
        txt = ' '.join(fake.sentences(3))
        pub = fake.year()
        c = random.randint(1, 20)
        obj = Book.objects.create(
            title=ttl,
            author=a,
            text=txt,
            published=pub,
            count=c
        )
        obj.save()
    # books = Book.objects.all()
    books = Book.objects.order_by('-id')
    return render(request, 'main/index.html', {'title': 'Головна сторінка', 'books': books})




def index(request):
    books = Book.objects.all()
    # books = Book.objects.order_by('-id')[:2]
    # books = Book.objects.filter(author='ГОСТ')
    # books = Book.objects.filter(id__gt=20)

    # books = Book.objects.filter(id__in=[1, 3, 4]))

    # q = Q(title__startswith='К') | ~Q(author__startswith='Г')
    # books = Book.objects.filter(q)

    return render(request, 'main/index.html', {'title': 'Головна сторінка', 'books': books})


def about(request):
    # return HttpResponse('<h1>Information about our project...</h1>')
    return render(request, 'main/about.html')


def start(request):
    return render(request, 'main/start.html')

def create(request):
    error = ''
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    form = BookForm()
    context = {
        'form': form
    }
    return render(request, 'main/create.html', context)

def book_view(request, id=1):
    book = Book.objects.get(id=id)
    return render(request, 'main/book_view.html', {'title': 'Книга', 'book': book})


def index_tab(request):
    books = Book.objects.all()
    return render(request, 'main/index_tab.html', {'title': 'Перелік книжок', 'books': books})


def book_edit(request, id=0):
    if request.method == 'GET':
        if id == 0:
            form = BookForm()
        else:
            book = Book.objects.get(id=id)
            form = BookForm(instance=book)
        return render(request, 'main/book_edit.html', {'form': form})
    else:
        if id == 0:
            form = BookForm(request.POST)
        else:
            book = Book.objects.get(id=id)
            form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
        return redirect('main')





    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    form = BookForm()
    context = {
        'form': form
    }
    return render(request, 'main/create.html', context)


def book_delete(request, id=0):
    book = Book.objects.get(id=id)
    book.delete()
    books = Book.objects.all()
    return render(request, 'main/index_tab.html', {'title': 'Перелік книжок', 'books': books})
