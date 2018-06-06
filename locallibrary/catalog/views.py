from django.shortcuts import render
from .models import Book, Author, Genre, BookInstance
from django.views import generic


class BookDetailView(generic.DetailView):
    model = Book

class BookListView(generic.ListView):
	model = Book
	paginate_by = 2

	# context_object_name = 'my_book_list'   # your own name for the list as a template variable
	# queryset = Book.objects.filter(title__icontains='days')[:5] # Get 5 books containing the title war
	# template_name = 'catalog/book_list.html'  # Specify your own template name/location

	def get_queryset(self):
		return Book.objects.filter()


class AuthorDetailView(generic.DetailView):
    model = Author


class AuthorListView(generic.ListView):
	model = Author
	paginate_by = 2

	def get_queryset(self):
		return Author.objects.filter()


def index(request):
	'''
	index page for the catalog app, as well as site
	'''
	num_books = Book.objects.all().count()
	num_instances = BookInstance.objects.all().count()

	# Available books (status = 'a')
	num_instances_available = BookInstance.objects.filter(status__exact='a').count()
	num_authors = Author.objects.all().count()

	num_geners = Genre.objects.all().count()

	context = {
		'num_books': num_books, 'num_instances': num_instances,
		'num_instances_available': num_instances_available,
		'num_authors': num_authors,
		'num_geners': num_geners,

	}
  
	return render(
		request,
		'index.html',
		context=context 
	)
