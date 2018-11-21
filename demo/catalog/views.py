from django.shortcuts import render
from django.http import HttpResponse
from django import forms

from .models import Supply, Clinic

# Create your views here.

class FormForSignIn(forms.Form):
    username = forms.CharField(label='username')
    password = forms.CharField(label='passname')

def signin(request):
    formForSignIn_obj = FormForSignIn()

    if request.method == 'POST':
        form_post = FormForReg(request.POST)
        if form_post.is_valid():
            print("data", form_post.cleaned_data)
        else:
            print("fail")
    else:
        print("Signin is not post")

    return render(
        request,
        'signin.html',
        context={'formForSignIn_obj': formForSignIn_obj,'link':'reg.html'},
    )

class FormForReg(forms.Form):
    ROLE_CHOICES=(
        ('c',"Clinic Manager"),
        ('w','Warehouse Personnel'),
        ('d','Dispatcher'),
        ('h','Hospital Authority')
    )

    CLINIC_CHOICES=[('a', '')]
    clinics= Clinic.objects.all()
    for clinic in clinics:
        CLINIC_CHOICES.append(tuple((str(clinic.name), str(clinic.name))))
    #print(CLINIC_CHOICES)

    username = forms.CharField(label='username')
    firstname = forms.CharField(label='firstname')
    lastname = forms.CharField(label='lastname')
    password = forms.CharField(label='password')
    email = forms.EmailField(label='email')
    role = forms.ChoiceField(label='role',choices=ROLE_CHOICES)
    clinic = forms.ChoiceField(label='clinic',choices=CLINIC_CHOICES,required=False)

    token = forms.CharField(label='token',required=False)

def registration(request):
    print("succeed")

    formForReg_obj = FormForReg()

    if request.method == 'POST':
        print("ok")
        form_post = FormForReg(request.POST)
        if form_post.is_valid():
            print("data", form_post.cleaned_data)
        else:
            print("fail")
    else:
        print("is not post")

    return render(
        request,
        'reg.html',
        context={'formForReg_obj': formForReg_obj},
    )

class FormForOrder(forms.Form):
    supply_list = Supply.objects.all()
    for supply in supply_list:
        supply.name = forms.IntegerField()

def clinicManager(request):
    supply_list = Supply.objects.all()
    formForOrder_obj = FormForOrder()

    return render(
        request,
        'clinic_manager_view.html',
        context={'supply_list': supply_list, "formForOrder_obj": formForOrder_obj},
    )

from django.http import JsonResponse
from django.contrib.auth.models import User

def validate_username(request):

    username = request.GET.get('username', None)
    print(username)
    data = {
        'is_taken': User.objects.filter(username__iexact=username).exists()
    }
    if data['is_taken']:
        data['error_message'] = 'A user with this username already exists.'

    return JsonResponse(data)

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