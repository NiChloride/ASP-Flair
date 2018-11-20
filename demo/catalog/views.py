from django.shortcuts import render
from django.http import HttpResponse

from .models import Supply

# Create your views here.
def supply(request):

    supply_number = Supply.objects.all().count()
    #print(supply_number)
    return render(
        request,
        'index.html',
        context={'supply_number': supply_number},
    )


"""
from .models import Book, Author, BookInstance, Genre

def index(request):
    
    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    num_authors = Author.objects.count()  # The 'all()' is implied by default.

    # Render the HTML template index.html with the data in the context variable
    return render(
        request,
        'index.html',
        context={'num_books': num_books, 'num_instances': num_instances,
                 'num_instances_available': num_instances_available, 'num_authors': num_authors},
    )

"""