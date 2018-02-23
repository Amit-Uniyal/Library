from django.shortcuts import render
from .models import Book, Author, Genre, BookInstance



def index(request):
	'''
	index page for the catalog app, as well as site
	'''
	num_books = Book.objects.all().count()
	num_instances = BookInstance.objects.all().count()

	# Available books (status = 'a')
	num_instances_available = BookInstance.objects.filter(status__exact='a').count()
	num_authors = Author.objects.all().count()

	context = {
		'num_books': num_books, 'num_instances': num_instances,
		'num_instances_available': num_instances_available,
		'num_authors': num_authors,

	}
  
	return render(
		request,
		'index.html',
		context=context 
	)
