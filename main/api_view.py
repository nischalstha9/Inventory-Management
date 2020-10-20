from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Order, OrderItem
from inventory.models import Item
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework.serializers import Serializer, SerializerMethodField

def add_to_cart(request, item_pk, qty):
    if qty>0:
        item = get_object_or_404(Item, pk = item_pk )
        order_item = OrderItem.objects.get_or_create(item=item,user = request.user,ordered = False)[0]
        print(order_item)
        order_qs = Order.objects.filter(user=request.user, status='NO')
        
        if order_qs.exists():
            order = order_qs[0]
            if order.items.filter(item__id = item_pk).exists():
                order_item.quantity += qty
                order_item.save()
            else:
                order.items.add(order_item)
                order_item.quantity = qty
                order_item.save()
        else:
            ordered_date = timezone.now()
            order = Order.objects.create(user=request.user, ordered_date = ordered_date)
            new_item = order.items.add(order_item)
            new_item.quantity = qty
            new_item.save()

@api_view(['POST'])
def create_order(request):
    current_user = request.user
    if request.method == 'POST':
        item_pk = int(request.data.get('item_id'))
        qty = int(request.data.get('qty'))
        add_to_cart(request, item_pk, qty)
        return Response({'order':'Order Created'})
    return Response({"message": "Data not received!"})

class OrderItemSerializer(Serializer):
    class Meta:
        model = OrderItem
        fields = ('item', 'quantity')

class CartDataSerializer(Serializer):
    item = SerializerMethodField()
    class Meta:
        model = Order
        fields = ('user','item')
    def get_item(self, obj):
        item_qs = OrderItem.objects.filter_by_object(obj)
        items = OrderItemSerializer(item_qs, many=True).data
        return items

import json
@api_view(['GET','POST'])
def api_cart(request):
    current_user = request.user
    if request.method == 'POST':
        qs = json.loads(request.data.get('data'))
        for i in qs:
            item_id = int(i['itemId'])
            qty = int(i['quantity'])
            order = Order.objects.get(user=request.user, status='NO')
            orderitem = order.items.get(item__id = item_id)
            if qty<=0:
                orderitem.delete()
            else:
                orderitem.quantity = qty
                orderitem.save()
    return Response('request.data')



# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import authentication, permissions
# from django.contrib.auth.models import User

# class ListUsers(APIView):
#     """
#     View to list all users in the system.

#     * Requires token authentication.
#     * Only admin users are able to access this view.
#     """
#     authentication_classes = [authentication.TokenAuthentication]
#     permission_classes = [permissions.IsAdminUser]

#     def get(self, request, format=None):
#         """
#         Return a list of all users.
#         """
#         usernames = [user.username for user in User.objects.all()]
#         return Response(usernames)