
from django.http import *
from django.template import loader
from django.shortcuts import render
from django import template
import  csv
from django.views.generic.list import *
from aspsite.models import *
from io import BytesIO
from reportlab.pdfgen import canvas
from django.urls import reverse
from datetime import *
from django.core.mail import *
from heapq import *
from random import *
# Create your views here.

##################################################LOGIN######################################################################################

def login(request):
    return render(request, 'login.html', {})

class login_handling(ListView): #returns a list of user
    model = User
    template_name = "user_page.html"

    def get_context_data(self, **kwargs): #context是传递到前端的数据集，以字典形式存在，比如context["user"]对应前端的{{user}}变量
        context = super().get_context_data(**kwargs)
        user = User.objects.get(id = self.request.COOKIES['user']) #modify 'user'
        context["user"] = user
        return context

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = User.objects.get(username = username)        #get the user object from database base by username
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


##################################################LOGIN######################################################################################
##################################################REGISTER###############################################################################
class register(ListView):
    model = Location
    template_name = "register.html"

def send_token(request):

    token_email = request.POST.get('email')
    try:
        token_object = Token.objects.get(email = token_email)
        send_mail('Your ASP Token For Registration',token_object.token,'aspflair@gmail.com',[token_object.email],fail_silently=False,)
    except Token.DoesNotExist:
        return HttpResponse("Your E-mail is not registered in AS-P system, contact the admin should you have any quiry")

    return HttpResponse("The Token Has Been Sent, Please Proceed in Registration")

def new_account(request):
    password = request.POST.get("password")
    token = request.POST.get("token")
    username = request.POST.get("username")
    firstName = request.POST.get("firstName")
    lastName = request.POST.get("lastName")
    location = request.POST.get("location")
    clinicLoc = Location.objects.get(id = location)

    if(not str(clinicLoc.category) == "Drone Port"): #check duplicated clinic manager accounts
        try:
            existing_user = User.objects.get(location = clinicLoc)
            return HttpResponse("Only one clinic manager is allowed for each clinic")
        except User.DoesNotExist:
            print("proceed")
    try:
        user_token = Token.objects.get(token = token)
    except Token.DoesNotExist:
        return HttpResponse("Wrong Token, please try again")

    user_token = Token.objects.get(token = token)

    try: #check duplicated email
        existing_user = User.objects.get(email = user_token.email)
        return HttpResponse("This email has been registered, go to forget password or contact admin")
    except User.DoesNotExist:
        print("milestone")


    try:
        user = User.objects.get(username = username)
        return HttpResponse("username has been taken")
    except User.DoesNotExist:
        user = User(first_name = firstName, 
        last_name = lastName, username = username, password = password,email = user_token.email,userType = user_token.userType)
        
        if (user.userType == "clinicManager"):
            user.clinic = clinicLoc
        else:
            user.clinic = Location.objects.get(category = "Drone Port")

        user.save()
        user_token.delete() #consume the token
        
        return HttpResponse("User has been successfully created")

    return HttpResponse("Duplicated username")


##################################################REGISTER###############################################################################



###################################################FORGET PASSWORD#########################################################################
def forgetPassword(request):
    return render(request, 'forget_password.html', {})

def generateToken(user):
    
    rand_token = randint(1000000000, 9999999999)
    newTokenObject =  Token(email = user.email, token = rand_token, userType = "reset_password_only")
    newTokenObject.save()
    return rand_token
def processResetPassword(request): #emails a randomly generated user token 
    request_username = request.POST.get("username")
    user = User.objects.get(username = request_username)
    token = generateToken(user)
    send_mail('ASP reset password token', str(token),'aspflair@gmail.com', [user.email], fail_silently=False,)
    #return HttpResponse("not yet implemented")
    return render(request, 'reset_password.html')

def resetPassword(request):
    request_email = request.POST.get("email")
    user = User.objects.get(email = request_email)
    entered_token = request.POST.get("token") #the token provided by the user
    new_password = request.POST.get("password")
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



###################################################FORGET PASSWORD#########################################################################
    



######################################################EDIT PROFILE##########################################################################
class ProfileView(ListView):
    model = User
    template_name = "profile.html"

    def get_context_data(self, **kwargs): #context是传递到前端的数据集，以字典形式存在，比如context["user"]对应前端的{{user}}变量
        context = super().get_context_data(**kwargs)

        #get the user data from database base on cookies
        user = User.objects.get(id = self.request.COOKIES['user'])

        #fetch the data from the database and feed to the page for rendering
        context["user"] = user
        return context


def edit_profile(request):
    #get the user object that need to change profile
    request_id = request.COOKIES['user']
    user = User.objects.get(id = request_id)
    #update user information
    user.password = request.POST.get("password")
    user.email = request.POST.get("email")
    user.firstname = request.POST.get("firstname")
    user.lastname = request.POST.get("lastname")
    user.save()

    return HttpResponse('Change Applied')

######################################################EDIT PROFILE##########################################################################

######################################################CLINIC MANAGER VIEWS###############################################################


class ItemDescriptionView(ListView):
    model = Item
    template_name = "item_descriptions.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["item"] = Item.objects.get(id = self.kwargs['itemid'])
        return context
    

class OrderView(ListView):
    model = Item
    template_name = "clinic_manager_view.html"
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = User.objects.get(id = self.request.COOKIES['user'])
        context["orders"] = Order.objects.filter(destination = context["user"].clinic)
        return context

def receive_confirmation(request):
    order = Order.objects.get(id = request.POST.get("orderID"))
    order.status = "Delivered"
    order.deliveredTime = datetime.now()
    order.save()
    return HttpResponseRedirect(reverse('clinic_manager_order'))


def place_order(request):
    item_list = Item.objects.all()
    manager = User.objects.get(id = request.POST.get("userid"))
    order = Order(creation_time=datetime.now(),status = "Queued for Processing",priority = request.POST.get("priority") )
    order.destination = manager.clinic
    order.save()
   
    if (len(item_list) == 0):
        order.delete()
        return HttpResponse("you did not order an item")

    for item in item_list:
        quantity = request.POST.get(str(item.id))

        while (int(quantity)>0):
            item_ordered = OrderItemMatching(order_id = order.id,item_id = item.id,quantity = quantity)
            item_ordered.save()
            break
    
    if order.total_weight()>25: #order exeeds max capacity of a drone
        order.delete()
        print("milestone")
        return HttpResponse("Cannot generate order: order exceeds maximum weight")

    return HttpResponseRedirect(reverse("clinic_manager_order"))

def cancel_order(request, orderid):
    Order.objects.get(id = orderid).delete()
    return HttpResponse('Successfully canceled order')
######################################################CLINIC MANAGER VIEWS###############################################################

#########################################################WAREHOUSE PERSEONNEL VIES##########################################################
class WarehousePersonnelView(ListView): #where warehouse Personnel views his order queue
    model = Order
    template_name = "warehouse_personnel_view.html"

    def get_queryset(self):
        return super().get_queryset().filter(status = 'Queued for Processing')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["process_queue "] = Order.objects.filter(status = 'Queued for Processing').order_by('-priority')
        #priority queue
        context["processing"] = Order.objects.filter(status = 'Processing by Warehouse')

        return context

class OrderItemsView(ListView):
    model = Order
    template_name = "order_items.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)    
        orderid = self.kwargs['orderid']
        context["order"] = Order.objects.get(id = orderid)
        return context

def sendShippingLabel(request):
    order = Order.objects.get(id = request.POST.get("orderID"))
    currentLine = 652
    buffer = BytesIO()
    drawingcanvas = canvas.Canvas(buffer)
    priority = ""
    if(int(order.priority)==3):
        priority = "High"
    elif(int(order.priority)==2):
        priority = "Medium"
    else:
        priority = "Low"
    drawingcanvas.drawString(120, currentLine, "Order Number: " + str(order.id))
    currentLine -= 43
    drawingcanvas.drawString(120, currentLine, "Order Time: " + str(order.creation_time))
    currentLine -= 43
    drawingcanvas.drawString(101, currentLine, "Priority: " + priority)
    currentLine -= 43
    drawingcanvas.drawString(120, currentLine, "Destination: " + str(order.destination.name))
    currentLine -= 43
    drawingcanvas.drawString(120, currentLine, "List of Items: ")
    
    for item in order.item_list.all():
        set_ = OrderItemMatching.objects.get(order_id = order.id, item_id = item.id)
        drawingcanvas.drawString(150, currentLine, item.name + ": " + str(set_.quantity))
        currentLine -= 43
    drawingcanvas.showPage()
    drawingcanvas.save()
    pdf = buffer.getvalue()
    buffer.close()
    clinic = order.destination
    managerEmail = User.objects.get(userType = 'clinicManager', clinic = clinic).email #send shipping label to every clinic manager
    email = EmailMessage(
        'Shipping Label',
        'Please find your shipping label in the attachment.',
        'aspflair@gmail.com',
        [managerEmail],
    )
    email.attach('order.pdf',pdf, 'application/pdf')
    email.send()
 
def packing(request): #packed button at warehouse personnel order page
    #get the order object
    sendShippingLabel(request) #one must send shipping label before packing
    order = Order.objects.get(id = request.POST.get("orderID"))
    order.status = 'Queued for Dispatch'
    order.save()
    return HttpResponseRedirect(reverse('warehouse_personnel_order'))
  
   

#########################################################WAREHOUSE PERSEONNEL VIES##########################################################

#########################################################DISPATCHER VIEWS####################################################################
class DispatcherView(ListView):
    model = Order
    template_name = "dispatcher_view.html"

    def get_queryset(self):
        return super().get_queryset().filter(status = 'Queued for Dispatch')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["packs"] =Drone.objects.all()

        return context
 
def path_finding_algorithm(locations):
    frontier = []
    heappush(frontier, (0, [Location.objects.get(category="Drone Port").id])) #(initialized total distance,[a list that stores the order in which destinations are visited, initially there is only the drone port])
    while (frontier):#while frontier is not empty (and it never should be)
        node = heappop(frontier)#get the first value in the heap, which has the shortest distance stored in route[0]
        unvisited = [x for x in locations if x not in node[1]]#locations that are not yet taken into consideration, initially there is only one location in route[1]
        if unvisited: #while there are still unconsidered locations
            for visit_next in unvisited:# for every unconsidered location visit_next
                heappush(frontier, (node[0]+Distance.objects.get(FROM_id = node[1][-1], TO_id = visit_next).distance, node[1]+[visit_next]))
                #add this location at the end of the location visit list, and add the resulting added distance travelled to route[0], which stores the total distance represented in route[1]
        else:
            return node[1] #every location is visited, thus return the one with shortest distance


def dispatch_selected(request): 
    selected_order = request.POST.getlist("orderID[]")
    order_list = []
    for orderid in selected_order:
        order_list.append(Order.objects.get(id = orderid))
    
    weight = 0
    for order in order_list:
        weight += order.total_weight()
    if(weight>25):
        return HttpResponse("Exceeds maximum capacity of drone")

    locations = []
    new_drone = Drone()
    new_drone.save()
    for order in order_list:
        
        new_drone.order.add(order)
        if (order.destination.id not in locations):
            locations.append(order.destination.id)
            print("order.destination.id: ",order.destination.id)
        order.status = "Dispatched"
        order.dispatchedTime = datetime.now()
        order.save()
    route = path_finding_algorithm(locations)
    route.append(Location.objects.get(category="Drone Port").id)

    for i in (range(len(route)-1)):
        itinerary = Distance.objects.get(FROM_id = route[i], TO_id = route[i+1])
        new_drone.itinerary.add(itinerary)

    new_drone.save()
    return HttpResponseRedirect(reverse('dispatcher_order'))



def download_itinerary(request):
   
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="route.csv"'

    writer = csv.writer(response)
    drone0 = Drone.objects.get(id = request.POST.get("packId"))
    writer.writerow(["Higher Visited First Latitude Longitude Altitude"])
    drone_port = Location.objects.get(category = "Drone Port")
    currentLocation = drone_port #from drone port takes off
    nextLocation = drone0.itinerary.get(FROM = currentLocation).TO
    while (nextLocation.category != "Drone Port"):
        #writer.writerow([nextLocation.name])
        writer.writerow([nextLocation.name, nextLocation.latitude, nextLocation.longitude, nextLocation.altitude]) 
        currentLocation = nextLocation
        nextLocation = drone0.itinerary.get(FROM = currentLocation).TO


    drone_port = Location.objects.get(category = "Drone Port")
    writer.writerow([drone_port .name, drone_port .latitude, drone_port .longitude, drone_port .altitude])
    #writer.writerow([source.name]) #return to drone port

    return response

def dispatch_drone(request): #dispatch drone
    drone0 = Drone.objects.get(id = request.POST.get("packId"))
     
    for order in drone0.order.all():   
        manager = User.objects.get(clinic=order.destination, userType="clinicManager")     
        order.dispatchedTime = datetime.now()
        order.save()
        send_mail('Your delivery is on the way', 'Order ID'+str(order.id)+' has been dispatched','aspflair@gmail.com', [manager.email], fail_silently=False,)
    drone0.delete()
    
    return HttpResponseRedirect(reverse('dispatcher_order'))

#########################################################DISPATCHER VIEWS####################################################################
class ClinicManagerView(ListView):
    model = Item
    template_name = "supply_items.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #fetch the context that the template works on

        #get theuser from url(done in urls.py)
        request_id = self.request.COOKIES['user'] #'user' is a key of the request

        #get the object for render
        context["user"] = User.objects.get(id = request_id)
        #returns a list of categories (in strings)

        return context

def process_order(request):
    order = Order.objects.get(id = request.POST["orderID"])
    order.status = 'Processing by Warehouse'
    order.save()
    return HttpResponseRedirect(reverse('warehouse_personnel_order'))

###############################################################LOOK NO FURTHER#################################################################
