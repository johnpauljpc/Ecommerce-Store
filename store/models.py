from django.conf import settings
from django.db import models
#from django.contrib.auth.models import User
from django.shortcuts import reverse
from django_countries.fields import CountryField

# Create your models here.
CATEGORY_CHOICES =(
		('S', 'Shirt'),
		('SW', 'Sport wear'),
		('OW', 'Out wear')
	)

LABEL_CHOICES =(
		('P', 'primary'),
		('S', 'secondary'),
		('D', 'danger')
	)

class Item(models.Model):
	title = models.CharField(max_length= 200)
	price = models.DecimalField(decimal_places = 0, max_digits = 10)
	discount_price = models.DecimalField(decimal_places = 0, max_digits = 10, null = True, blank = True)
	category = models.CharField(choices = CATEGORY_CHOICES, max_length = 5)
	label = models.CharField(choices = LABEL_CHOICES, max_length = 5)
	slug = models.SlugField()
	description = models.TextField()


	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse("product", kwargs={'slug':self.slug})

	def get_add_to_cart_url(self):
		return reverse("add-to-cart", kwargs={'slug':self.slug})	

class OrderItem(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	item = models.ForeignKey(Item, on_delete = models.CASCADE) 
	quantity = models.IntegerField(default=1)
	ordered = models.BooleanField(default=False)

	def __str__(self):
		return f'{self.quantity} quantity of {self.item.title}'

	def get_total_item_price(self):
		total = (self.quantity) * (self.item.price)
		return total

	def get_total_item_discount_price(self):
		total = (self.quantity) * (self.item.discount_price)
		return total

	def amount_saved(self):
		saved = self.get_total_item_price() - self.get_total_item_discount_price()
		return saved

	def get_precise_total(self):
		if  self.item.discount_price:
			return self.get_total_item_discount_price()
		return self.get_total_item_price()


class Order(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	items = models.ManyToManyField(OrderItem)
	start_date = models.DateTimeField(auto_now_add = True)
	ordered_date = models.DateTimeField()
	ordered = models.BooleanField(default=False)
	billing_address = models.ForeignKey('BillingAddress', on_delete = models.SET_NULL, blank = True, null = True )


	def __str__(self):
		return self.user.username

	def get_absolute_url(self):
		return reverse("order-summary", kwargs={'pk':self.id})

	def order_total(self):
		total = 0
		for order_item in self.items.all():
			total += order_item.get_precise_total()
		return total

PAYMENT_CHOICES =(
	('S', 'Stripe'),
	('P', 'Paypal')
	)
class BillingAddress(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	street_address = models.CharField( max_length = 100)
	appartment_address = models.CharField( max_length = 100)
	country = CountryField(multiple = False)
	zipcode = models.IntegerField()
	#same_billing_address = models.BooleanField(blank = True, null = True)
	#save_info = models.BooleanField(blank = True, null = True)
	#payment_option = models.CharField(choices=PAYMENT_CHOICES)


	def __str__(self):
 		return self.user.username