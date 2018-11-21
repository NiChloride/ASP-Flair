from django.contrib.auth.models import Group
from django.shortcuts import render
from django.http import HttpResponse
from django import forms
from django.contrib.auth import get_user_model
from .models import Supply, Clinic
from .models import UserProfile
from django.http import HttpResponseRedirect
from django.contrib import auth
# Create your views here.


class FormForSignIn(forms.Form):
    username = forms.CharField(label='username')
    password = forms.CharField(label='password')

def signin(request):
    formForSignIn_obj = FormForSignIn()

    if request.method == 'POST':
        print("POST")
        form_post = FormForSignIn(request.POST)
        if form_post.is_valid():

            #print("data", form_post.cleaned_data)
            print("valid!")
            username = form_post.cleaned_data['username']
            password = form_post.cleaned_data['password']
            print(username)
            print(password)
            luser = auth.authenticate(username=username, password=password)
            #print(luser.role)
            if luser is not None and luser.is_active:
                auth.login(request, luser)
                userprofile_obj = UserProfile.objects.get(user = luser)
                if(userprofile_obj.role == "ClinicManager"):
                    return HttpResponseRedirect("catalog/c/")


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
        ("ClinicManager","Clinic Manager"),
        ('WarehousePersonnel','Warehouse Personnel'),
        ('Dispatcher','Dispatcher'),
        ('HospitalAuthority','Hospital Authority')
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
            username = form_post.cleaned_data['username']
            password = form_post.cleaned_data['password']
            email = form_post.cleaned_data['email']
            firstname = form_post.cleaned_data['firstname']
            lastname = form_post.cleaned_data['lastname']
            clinic = form_post.cleaned_data['clinic']
            token = form_post.cleaned_data['token']
            role = form_post.cleaned_data['role']
            user = User.objects.create_user(username=username, password=password, email=email,first_name=firstname,last_name=lastname)
            user_profile = UserProfile(user=user, role=role, clinic = clinic)
            user_profile.save()
            his_group = Group.objects.get(name=role) 
            his_group.user_set.add(user)

            #User.objects.create(username=username,password=password,email=email,first_name = firstname, last_name = lastname, clinic = clinic, token = token)
            #User.save()
            return HttpResponseRedirect("/catalog/")



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