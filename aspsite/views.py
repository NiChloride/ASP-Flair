from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect, FileResponse
from django.template import loader
from django import template

from easy_pdf.views import PDFTemplateView
from aspsite.models import *
from io import BytesIO
from reportlab.pdfgen import canvas
import io,  csv
from django.urls import reverse
from django.views.generic.list import ListView
from datetime import *
from django.core.mail import *
from heapq import *
from random import *
# Create your views here.

#main page

def mainpage(request):
    return render(request, 'login.html', {})

#forget password page
  
def forgetPassword(request):
    return render(request, 'forgotPassword.html', {})

def generateToken(user):
    
    rand_token = randint(1000000000, 9999999999)
    newTokenObject =  Token(email = user.email, token = rand_token, userType = "reset_password_only")
    newTokenObject.save()
    return rand_token
def processResetPassword(request): #emails a randomly generated user token 
    request_username = request.POST["userID"]
    user = User.objects.get(userID = request_username)
    token = generateToken(user)
    send_mail('ASP reset password token', str(token),'aspflair@gmail.com', [user.email], fail_silently=False,)
    #return HttpResponse("not yet implemented")
    return render(request, 'resetPassword.html')

def resetPassword(request):
    request_email = request.POST["email"]
    user = User.objects.get(email = request_email)
    entered_token = request.POST["token"] #the token provided by the user
    new_password = request.POST["password"]
    reset_token = Token.objects.get(email=request_email,userType="reset_password_only").token
    
    if(entered_token==reset_token):
        user.password = new_password
        user.save()
        Token.objects.get(email=request_email,userType="reset_password_only").delete()
        return HttpResponse("Password Successfully Updated")
    else:
        Token.objects.get(email=request_email,userType="reset_password_only").delete()
        return HttpResponse("Invalid Token")



    #return render()
    return HttpResponse("not yet implemented")


class register(ListView):
    model = Location
    template_name = "register.html"

    
class login_handling(ListView):
    model = User
    template_name = "user_page.html"

    def get_context_data(self, **kwargs): #context是传递到前端的数据集，以字典形式存在，比如context["user"]对应前端的{{user}}变量
        context = super().get_context_data(**kwargs)

        #get the user data from database base on cookies
        user = User.objects.get(id = self.request.COOKIES['user'])

        #fetch the data from the database and feed to the page for rendering
        context["user"] = user
        return context

    def post(self, request, *args, **kwargs):
        username = request.POST['userID']
        password = request.POST['password']
        try:
            #get the user object from database base by username
            user = User.objects.get(userID = username)
        except User.DoesNotExist:
            return HttpResponse('wrong username or password')
        
        #password matching
        if (user.password == password):
            #correct 
            output = render(request, 'user_page.html', {'user' : user})
            
            output.set_cookie('user', user.id)

            return output
        else:
            #incorrect credentials
            return HttpResponse('wrong username or password')


#profile page
class Profile(ListView):
    model = User
    template_name = "profile.html"

    def get_context_data(self, **kwargs): #context是传递到前端的数据集，以字典形式存在，比如context["user"]对应前端的{{user}}变量
        context = super().get_context_data(**kwargs)

        #get the user data from database base on cookies
        user = User.objects.get(id = self.request.COOKIES['user'])

        #fetch the data from the database and feed to the page for rendering
        context["user"] = user
        return context






class clinicManagerItem(ListView):
    model = Item
    template_name = "clinicManagerItems.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #fetch the context that the template works on

        #get theuser from url(done in urls.py)
        request_id = self.request.COOKIES['user'] #'user' is a key of the request

        #get the object for render
        context["user"] = User.objects.get(id = request_id)
        #returns a list of categories (in strings)

        return context

class clinicManagerDescription(ListView):
    model = Item
    template_name = "clinicManagerDescription.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        #get the data from urls(done in urls.py)
        itemid = self.kwargs['itemid']

        #get the object for render
        context["item"] = Item.objects.get(id = itemid)
        return context
    

class clinicManagerOrder(ListView):
    model = Item
    template_name = "clinicManagerOrder.html"
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        #get the data from urls(done in urls.py)
        request_id = self.request.COOKIES['user']

        #get the object for render
        context["user"] = User.objects.get(id = request_id)
        context["orders"] = Order.objects.filter(location = context["user"].clinic)

        return context

def receive_confirmation(request):
    orderid = request.POST["orderId"]
    order = Order.objects.get(id = orderid)

    order.status = "Delivered"
    order.deliveredTime = datetime.now()

    order.save()

    return HttpResponseRedirect(reverse('clinic_manager_order'))

class warehousePersonnelOrder(ListView):
    model = Order
    template_name = "warehousePersonnelOrder.html"

    def get_queryset(self):
        return super().get_queryset().filter(status = 'Queued for Processing')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["queue"] = Order.objects.filter(status = 'Queued for Processing').order_by('-priority')

        context["processing"] = Order.objects.filter(status = 'Processing by Warehouse')

        return context


class warehousePersonnelChecklist(ListView):
    model = Order
    template_name = "warehousePersonnelChecklist.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)    
        orderid = self.kwargs['orderid']
        context["order"] = Order.objects.get(id = orderid)
        return context

class dispatcherOrder(ListView):
    model = Order
    template_name = "dispatcherOrder.html"

    def get_queryset(self):
        return super().get_queryset().filter(status = 'Queued for Dispatch')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["packs"] =Pack.objects.all()

        return context
        

class TokenView(ListView):
    model = Token #处理一个普通对象或者Queryset 时，Django 能使用其模型类的小写名称来放入Context，此处为context["token"]
    template_name = "token.html"

def send_token(request):

    token_email = request.POST['email']
    try:
        token_object = Token.objects.get(email = token_email)
        send_mail('Your ASP Token For Registration',token_object.token,'aspflair@gmail.com',[token_object.email],fail_silently=False,)
    except Token.DoesNotExist:
        return HttpResponse("Your E-mail is not registered in AS-P system, contact the admin should you have any quiry")

    return HttpResponse("The Token Has Been Sent, Please Proceed in Registration")
    

def changeProfile(request):
    #get the user object that need to change profile
    request_id = request.COOKIES['user']
    user = User.objects.get(id = request_id)
    #update user information
    user.password = request.POST["password"]
    user.email = request.POST["email"]
    user.firstname = request.POST["firstname"]
    user.lastname = request.POST["lastname"]
    user.save()

    return HttpResponse('Change Applied')

def makeOrder(request):
    items = Item.objects.all()
    user = User.objects.get(id = request.POST.get("userid"))

    order = Order()
    order.status = "Queued for Processing"
    order.priority = request.POST["priority"]
    order.location = user.clinic
    order.save()
    totalNo = 0
    for item in items:
        quantity = request.POST.get(str(item.id))
        totalNo += int(quantity)

    if (totalNo == 0):
        order.delete()
        return HttpResponse("please input a valid number")

    for item in items:
        quantity = request.POST.get(str(item.id))

        if (quantity != '0'):
            item_ordered = Order_Item()
            item_ordered.order_id = order.id
            item_ordered.item_id = item.id
            item_ordered.quantity = quantity
            item_ordered.save()
    if order.getCombinedWeight()>25:
        order.delete()
        return HttpResponse("Cannot generate order: order exceeds maximum weight")

    return HttpResponseRedirect(reverse("clinic_manager_order"))




def cancel_order(request, orderid):

    #delete the order
    order = Order.objects.get(id = orderid)
    order.delete()

    return HttpResponse('Successfully canceled order')

def processOrder(request):
    #get the order object
    orderId = request.POST["orderId"]
    order = Order.objects.get(id = orderId)

    #update the status
    order.status = 'Processing by Warehouse'

    #save the object
    order.save()

    return HttpResponseRedirect(reverse('warehouse_personnel_order'))

def pack(request): #packed button at warehouse personnel order page
    #get the order object
    orderId = request.POST["orderId"]
    order = Order.objects.get(id = orderId)

    #update the status
    order.status = 'Queued for Dispatch'

    #save the object
    order.save()

    return HttpResponseRedirect(reverse('warehouse_personnel_order'))

def optimalRoute(locations):
    frontier = []
    heappush(frontier, (0, [Location.objects.get(category="Drone Port").id])) #0 is the initialized total distance, [1] means now there is location with id 1 in the route
    while (frontier):
        node = heappop(frontier)
        unvisited = [x for x in locations if x not in node[1]]
        if unvisited:
            for nextnode in unvisited:
                heappush(frontier, (node[0]+Distance.objects.get(location1_id = node[1][-1], 
                location2_id = nextnode).distance, node[1]+[nextnode]))
        else:
            return node[1] #every location is visited, thus return the one with shortest distance


def dispatch_selected(request): 
    selected_order = request.POST.getlist("orderId[]")
    locations = []
    pack = Pack()
    pack.save()
    for orderid in selected_order:
        order = Order.objects.get(id = orderid)
        pack.order.add(order)
        if (order.location.id not in locations):
            locations.append(order.location.id)
            print("order.location.id: ",order.location.id)
        order.status = "Dispatched"
        order.dispatchedTime = datetime.now()
        order.save()

    route = optimalRoute(locations)

    route.append(Location.objects.get(category="Drone Port").id)

    for i in (range(len(route)-1)):
        itinerary = Distance.objects.get(location1_id = route[i], location2_id = route[i+1])
        pack.itinerary.add(itinerary)

    pack.save()
    return HttpResponseRedirect(reverse('dispatcher_order'))



def download_itinerary(request):
    # Output CSV file containing itinerary information
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="route.csv"'

    writer = csv.writer(response)
    pack = Pack.objects.get(id = request.POST["packId"])
    writer.writerow(["Higher Visited First "])
    currentLocation = Location.objects.get(category = "Drone Port") #from drone port takes off
    nextLocation = pack.itinerary.get(location1 = currentLocation).location2
    while (nextLocation.category != "Drone Port"):
        #writer.writerow([nextLocation.name])
        writer.writerow([nextLocation.name, nextLocation.latitude, nextLocation.longitude, nextLocation.altitude]) 
        currentLocation = nextLocation
        nextLocation = pack.itinerary.get(location1 = currentLocation).location2


    source = Location.objects.get(category = "Drone Port")
    writer.writerow([source.name, source.latitude, source.longitude, source.altitude])
    #writer.writerow([source.name]) #return to drone port

    return response

def dispatch_drone(request): #dispatch drone
    pack = Pack.objects.get(id = request.POST["packId"])

    for order in pack.order.all():        
        order.dispatchedTime = datetime.now()
        order.save()
    pack.delete()
    return HttpResponseRedirect(reverse('dispatcher_order'))








def sendShippingLabel(request):
    #get the order object
    orderId = request.POST["orderId"]
    order = Order.objects.get(id = orderId)

    currentLine = 750
    

    # Create a file-like buffer to receive PDF data.
    '''
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="label' + str(order.id) + '.pdf"'
    '''
    #response = HttpResponse(content_type='application/pdf')
    #response['Content-Disposition'] = 'attachment; filename="order.pdf"'
    #write into buffer
    response = HttpResponse("Label Sent")
    buffer = BytesIO()
    p = canvas.Canvas(buffer)
    priority = ""
    if(int(order.priority)==3):
        priority = "High"
    elif(int(order.priority)==2):
        priority = "Medium"
    else:
        priority = "Low"
    p.drawString(100, currentLine, "OrderID: " + str(order.id))
    currentLine -= 50
    p.drawString(100, currentLine, "Priority: " + priority)
    currentLine -= 50
    p.drawString(100, currentLine, "Location: " + str(order.location.name))
    currentLine -= 50
    p.drawString(100, currentLine, "Items: ")
    # currentLine -= 50
    #drawing each item
    for item in order.items.all():
        set_ = Order_Item.objects.get(order_id = order.id, item_id = item.id)
        p.drawString(150, currentLine, item.name + ": " + str(set_.quantity))
        currentLine -= 50

    p.showPage()
    p.save()
    pdf = buffer.getvalue()
    buffer.close()

    clinic = order.location
    managerEmail = User.objects.get(userType = 'clinicManager', clinic = clinic).email #send shipping label to every clinic manager
    email = EmailMessage(
        'Shipping Label',
        'Please find your shipping label in the attachment.',
        'aspflair@gmail.com',
        [managerEmail],
    )
    email.attach('order.pdf',pdf, 'application/pdf')
    email.send()

    #response.write(pdf)
    return response






def new_account(request):

  
    password = request.POST["password"]
    token = request.POST["token"]
    username = request.POST["userID"]
    firstName = request.POST["firstName"]
    lastName = request.POST["lastName"]
    location = request.POST["location"]

    try:
        user_token = Token.objects.get(token = token)
    except Token.DoesNotExist:
        return HttpResponse("No such token")

    try:
        user_ = User.objects.get(userID = username)
    except User.DoesNotExist:
        user = User(first_name = firstName, 
        last_name = lastName, userID = username, password = password,email = user_token.email,userType = user_token.userType)
        
        if (user.userType == "clinicManager"):
            user.clinic = Location.objects.get(id = location)
        else:
            user.clinic = Location.objects.get(category = "Drone Port")

        user.save()
        
        return HttpResponse("User has been successfully created")

    return HttpResponse("Duplicated user ID")



    

    




    

    
