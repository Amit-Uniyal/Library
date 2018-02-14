import uuid
from django.db import models
from django.urls import reverse


class Genre(models.Model):
    name = models.CharField(max_length=200, help_text="Enter a book genre(e.g. Science Fiction, French Poetry etc.)")

    def __str__(self):
        return self.name

class Author(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)

    class Meta:
        ordering = ["last_name", "first_name"]

    def get_absolute_url(self):
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        return '{0},{1}'.format(self.first_name, self.last_name)

class Book():
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True)
    summary = models.TextField(max_length=1000, help_text="Enter a brief description of the book")
    isbn = models.CharField('ISBN', max_length=13, help_text="13 character")
    genre = models.ManyToManyField(Genre, help_text="Select genre for this book")

    def _get_absolute_url_(self):
        '''
         /application/modelname/2
         where 2 is a id in record

        :return: The url to access a particular instance of the model
        '''
        return reverse('book-detail', args=[str(self.id)])

        def __str__(self):
            return self.title.capitalize()

class BookInstance(models.Model):
    '''
    Model represent specific copy of a book
    '''
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique id for this particular book across whole library")
    book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)

    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default='m', help_text='Book Availability')

    class Meta:
        ordering = ['due_back']

    def __str__(self):
        return '{0} ({1})'.format(self.id, self.book.title)

