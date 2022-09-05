from django.conf import settings
from django.db import models
from django.shortcuts import reverse

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


class Order(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	items = models.ManyToManyField(OrderItem)
	start_date = models.DateTimeField(auto_now_add = True)
	ordered_date = models.DateTimeField()
	ordered = models.BooleanField(default=False)


	def __str__(self):
		return self.user.username