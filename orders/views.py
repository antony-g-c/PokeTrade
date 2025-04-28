from django.shortcuts import render, get_object_or_404
from .models import Order

def order_list(request):
    orders = request.user.orders.all()
    return render(request, 'orders/list.html', {'orders': orders})

def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk, user=request.user)
    return render(request, 'orders/detail.html', {'order': order})
