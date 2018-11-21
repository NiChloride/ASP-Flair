from django.db import models
from django.utils.html import mark_safe
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User

# Create your models here.

class Supply(models.Model):
    """
    Model representing a supply
    """
    name = models.CharField(max_length=200, help_text="Enter a supply name with max length 200")

    weight = models.FloatField(help_text="Enter the weight of supply")

    image = models.ImageField( help_text="Upload a image of supply")

    category = models.ForeignKey("Category",on_delete=models.SET_NULL, null=True)
    #category !!!!
    def __str__(self):
        """
        representing supply
        """
        return self.name

class Category(models.Model):

    name = models.CharField(max_length=200, help_text="Enter category name with max length 200")

    def __str__(self):
        """
        representing supply
        """
        return self.name

class Order(models.Model):
    """
    Model representing a order
    """
    order_id = models.AutoField(primary_key=True)

    weight = models.FloatField(editable=False , default=0.0)

    ORDER_STATUS = (
        ('qp', 'Queued for Processing'),
        ('pw', 'Processing by WareHouse'),
        ('qd', 'Queued for Dispatching'),
        ('di', 'Dispatched'),
        ('de', 'Delivered')
    )
    status = models.CharField(max_length=2 , choices=ORDER_STATUS, blank=True, default='dq', help_text='Order status')

    orderedtime = models.DateTimeField(null=True, blank=True)

    dispatchedtime = models.DateTimeField(null=True, blank=True)

    arrivedtime = models.DateTimeField(null=True, blank=True)

    destination = models.ForeignKey("Clinic", on_delete=models.SET_NULL, null=True )

    PRIORITY_STATUS = (
        ('a','High'),
        ('b', 'Medium'),
        ('c', 'Low')
    )

    priority = models.CharField(max_length=1, choices=PRIORITY_STATUS, help_text="Enter priority.")

    class Meta:
        ordering = ['priority','order_id']

    def __str__(self):
        """
        String for representing the Order object
        """
        return str(self.order_id)

class Clinic(models.Model):
    """
    Model representing a clinic
    """
    name = models.CharField(max_length=200, help_text="Enter the clinic name with max length 200", primary_key=True)

    latitude = models.FloatField(help_text="latitude for clinic")

    longitude = models.FloatField(help_text="longitude for clinic")

    altitude = models.FloatField(help_text="altitude for clinic")

    def __str__(self):
        """
        String for representing the Model object (in Admin site etc.)
        """
        return self.name

class DistanceBetween2Clinics(models.Model):
    
    clinicA = models.ForeignKey(Clinic, on_delete=models.SET_NULL, null=True,related_name='clinicA')

    clinicB = models.ForeignKey(Clinic, on_delete=models.SET_NULL, null=True,related_name='clinicB')

    distance = models.FloatField(help_text="distance in km")

    def __str__(self):
       
        return self.clinicA.name+" "+self.clinicB.name


class OrderSupplyMatching(models.Model):
    """
    Model Order and Supply matchings
    """
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=False, editable=False)

    supply = models.ForeignKey(Supply, on_delete=models.CASCADE, null=False)

    numberofsupply = models.IntegerField(default=0,help_text="Number of supply needed")

    def save(self, *args, **kw):
        #edit before
        super(OrderSupplyMatching,self).save(*args,**kw)
        self.order.weight+=self.supply.weight * self.numberofsupply
        self.order.save()
        #edit after

    def __str__(self):
        """
        String for representing the Model object (in Admin site etc.)
        """
        return str(self.order.order_id)+'  :  '+self.supply.name+" * "+str(self.numberofsupply)


class Drone(models.Model):

    maxweight = models.FloatField(help_text="Enter the max weight of drone")

    order = models.ManyToManyField(Order,help_text="Select order for this drone")

    #csvfile = models.FileField(editable=False)


class UserProfile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')

    role = models.CharField(max_length=50)
    
    clinic = models.CharField(max_length=50)
    
    token = models.CharField(max_length=50,blank=True)

    class Meta:
        verbose_name = 'User Profile'

    def __str__(self):
        return self.user.__str__()


