from django.shortcuts import render
from .models import Book, Author, Genre, BookInstance
from django.views import generic

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

# authentication restriction
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import permission_required


# forms
from django.http import HttpResponseRedirect
from django.urls import reverse
import datetime
from .forms import RenewBookForm
from django.shortcuts import get_object_or_404

# Post data

class AuthorCreate(CreateView):
    model = Author
    fields = '__all__'
    initial={'date_of_death':'05/01/2018',}

class AuthorUpdate(UpdateView):
    model = Author
    fields = ['first_name','last_name','date_of_birth','date_of_death']

class AuthorDelete(DeleteView):
    model = Author
    success_url = reverse_lazy('authors')

class BookCreate(CreateView):
    model = Book
    fields = '__all__'

class BookUpdate(UpdateView):
    model = Book
    fields = '__all__'

class BookDelete(DeleteView):
    model = Book
    success_url = reverse_lazy('books')


# Listing
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

@login_required
def index(request):
	# index page for the catalog app, as well as site

    # Sessions
    # number of visits to this view, as counted in session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] =num_visits+1

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
        'num_visits': num_visits,

	}
    return render(
		request,
		'index.html',
		context=context 
	)

class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
    """
    Generic class-based view listing books on loan to current user.
    """
    model = BookInstance
    template_name ='catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 2

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')

@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request, pk):
    book_inst=get_object_or_404(BookInstance, pk = pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = RenewBookForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            book_inst.due_back = form.cleaned_data['renewal_date']
            book_inst.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('all-borrowed') )

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date,})

    return render(request, 'catalog/book_renew_librarian.html', {'form': form, 'bookinst':book_inst})