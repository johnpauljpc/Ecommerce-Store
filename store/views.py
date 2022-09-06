from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Item, OrderItem, Order
from django.views.generic import DetailView, ListView
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
	paginate_by = 1
	context_object_name = 'products'
	template_name = 'home-page.html'


class ItemDetailView(DetailView):
	model = Item
	context_object_name = 'products'
	template_name = 'product-page.html'


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

	return redirect (reverse('product', kwargs={'slug':slug}), {'messages':messages})



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
			return redirect (reverse('product', kwargs={'slug':slug}), {'messages':messages})


	else:
		#Add a message saying the user doesnt have an order
		messages.info(request, "You do not have an order of this product")
		return redirect (reverse('product', kwargs={'slug':slug}), {'messages':messages})


	return redirect (reverse('product', kwargs={'slug':slug}), {'messages':messages})


