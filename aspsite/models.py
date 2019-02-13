from django.db import models



class Item(models.Model):
	category = models.ForeignKey('ItemCategory',on_delete=models.CASCADE, related_name='category',null = True)
	#category = models.ForeignKey('ItemCategory',on_delete=models.CASCADE, related_name='category')
	name = models.CharField(max_length=30)
	description = models.CharField(max_length=50)
	unitWeight = models.DecimalField(max_digits=6, decimal_places=3)
	image = models.ImageField()
	def __str__(self):
		return '{} {} {} {}'.format(self.category,self.name, self.description, self.unitWeight)

class Distance(models.Model):
    FROM = models.ForeignKey('Location', on_delete=models.CASCADE, related_name='FROM')
    TO = models.ForeignKey('Location', on_delete=models.CASCADE, related_name='TO')
    distance = models.DecimalField(max_digits=5, decimal_places=2)
    def __str__(self):
    	return '{} {} {}'.format(self.FROM,self.TO,self.distance)

class Location(models.Model):
	category = models.CharField(max_length=30)
	group = models.CharField(max_length=30)
	name = models.CharField(max_length=50)
	latitude = models.DecimalField(max_digits=11, decimal_places=6)
	longitude = models.DecimalField(max_digits=11, decimal_places=6)
	altitude = models.IntegerField()
	Distance = models.ManyToManyField("self", through='Distance', through_fields=('FROM', 'TO'), symmetrical=False)
	def __str__(self):
		return '{}'.format(self.name)

class Order(models.Model):
	creation_time = models.DateTimeField(null = True)
	status = models.CharField(max_length=30)
	priority = models.IntegerField()
	item_list = models.ManyToManyField(Item, through='OrderItemMatching')
	destination = models.ForeignKey(Location, on_delete=models.CASCADE)
	dispatchedTime = models.DateTimeField(null = True)
	deliveredTime = models.DateTimeField(null = True)
	def __str__(self):
		return '{} {}'.format(self.destination,self.status, self.priority)

	def total_weight(self):
		totalWeight = 0.0
		for item in self.items.all():
			totalWeight += float(item.unitWeight) * OrderItemMatching.objects.get(item_id = item.id, order_id = self.id).quantity
		return totalWeight

class OrderItemMatching(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    def __str__(self):
    	return '{} {} {}'.format(self.quantity, self.item, self.order)



class User(models.Model):
	username = models.CharField(max_length=50)
	password = models.CharField(max_length=20)
	email = models.EmailField()
	clinic = models.ForeignKey('Location', on_delete=models.CASCADE, null = True)
	first_name = models.CharField(max_length=30)
	last_name = models.CharField(max_length=30)
	userType = models.CharField( max_length=20)
	def __str__(self):
		return '{} {} {} {} {}'.format(self.userID, self.email, self.clinic, self.first_name, self.last_name)

class Drone(models.Model):
	order = models.ManyToManyField(Order)
	itinerary = models.ManyToManyField(Distance)


class Token(models.Model):
	token = models.CharField(max_length=10)
	email = models.EmailField()
	userType = models.CharField(max_length=20)


class ItemCategory(models.Model):
	name = models.CharField(max_length=30)
	def __str__(self):
		return '{}'.format(self.name)

	

