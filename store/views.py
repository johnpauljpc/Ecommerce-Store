from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin 
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from .models import Item, OrderItem, Order
from django.views.generic import (DetailView,
View, ListView)
from django.urls import reverse
from django.utils import timezone

# Create your views here.
def products(request):
	items = Item.objects.all()
	context = {'items':items}

	return render(request,'product-page.html', context)


def checkout(request):

	context = {}

	return render(request, 'checkout-page.html', context)


def home(request):

	context = {}

	return render(request, 'home-page.html', context)

class HomeView(ListView):
	model = Item
	paginate_by = 2
	context_object_name = 'products'
	template_name = 'home-page.html'

class OrderSummaryView(LoginRequiredMixin, View):
	#model = Order
	#context_object_name = 'orders'
	#template_name = 'order_summary.html'

	def get(self, *args, **kwargs):

		try:
			order = Order.objects.get(user = self.request.user, ordered = False )
			context = {
                'object': order
            }
			return render(self.request, 'order_summary.html', context)
		except ObjectDoesNotExist:
			messages.error(request, "You do not have an active order")
			return redirect('/')
		return render(self.request, 'order_summary.html')

class ItemDetailView(DetailView):
	model = Item
	context_object_name = 'products'
	template_name = 'product-page.html'

@login_required
def add_to_cart(request, slug):

	item = get_object_or_404(Item, slug = slug)
	order_item, created = OrderItem.objects.get_or_create(item = item,
		user = request.user, ordered =False)
	order_qs = Order.objects.filter(user = request.user, ordered = False)
	if order_qs.exists():
		order = order_qs[0]
		# chwck if the order item is in the order
		if order.items.filter(item__slug=item.slug).exists():
			order_item.quantity += 1
			order_item.save()
			messages.success(request, "The quantity of this item was updated")
		else:
			messages.info(request, "This item was added to your cart")
			order.items.add(order_item)
	else:
		ordered_date = timezone.now()
		order = Order.objects.create(user = request.user, ordered_date = ordered_date)
		order.items.add(order_item)

	return redirect ('order-summary')


@login_required
def remove_from_cart(request, slug):
	item = get_object_or_404(Item, slug = slug)
	order_qs = Order.objects.filter(user = request.user, ordered = False)
	if order_qs.exists():
		order = order_qs[0]
		# chwck if the order item is in the order
		if order.items.filter(item__slug=item.slug).exists():
			order_item = OrderItem.objects.filter(item = item,
				user = request.user, ordered = False)[0]
			order.items.remove(order_item)
			messages.warning(request, "You have removed an item from your cart")
		else:
			#Add a message saying the order doesnt contain that item
			messages.info(request, "This order doesn't contain the item")
			return redirect ('order-summary')


	else:
		#Add a message saying the user doesnt have an order
		messages.info(request, "You do not have an order of this product")
		return redirect ('order-summary')


	return redirect (reverse('product', kwargs={'slug':slug}), {'messages':messages})


@login_required
def remove_single_item_from_cart(request, slug):
	item = get_object_or_404(Item, slug = slug)
	order_qs = Order.objects.filter(user = request.user, ordered = False)
	if order_qs.exists():
		order = order_qs[0]
		# chwck if the order item is in the order
		if order.items.filter(item__slug=item.slug).exists():
			order_item = OrderItem.objects.filter(item = item,
				user = request.user, ordered = False)[0]
			#order.items.remove(order_item)
			if order_item.quantity > 1:
				order_item.quantity -= 1
				order_item.save()
			else:
				order_item.delete()
				# or order.items.remove(order_item)

			messages.warning(request, "quantity of item has been reduced from your cart")
			return redirect ('order-summary' )
		else:
			#Add a message saying the order doesnt contain that item
			messages.info(request, "This order doesn't contain the item") 
			return redirect ('order-summary' )


	else:
		#Add a message saying the user doesnt have an order
		messages.info(request, "You do not have an order of this product")
		return redirect('order-summary')


	

