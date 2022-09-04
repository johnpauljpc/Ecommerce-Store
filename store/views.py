from django.shortcuts import render
from .models import Item, OrderItem, Order

# Create your views here.
def item_list(request):
	items = Item.objects.all()
	context = {'items':items}

	return render(request,'home-page.html', context)