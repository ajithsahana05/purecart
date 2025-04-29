from django.shortcuts import render
from django.db.models import Q
from django.http import JsonResponse,HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.generics import RetrieveAPIView
from rest_framework.generics import UpdateAPIView
from rest_framework.generics import DestroyAPIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from .serializers import *
from .models import *
from rest_framework.views import APIView
import random,time

class ProductCreation(CreateAPIView):
    serializer_class = ProductsSerializer
    permission_classes = (AllowAny,)
    userinfo = Products.objects.all()
    def post(self, request):
        try:
            if request.FILES['image_url']:
                print("Yes")
            else:
                print("No")
            form = ProductForm(request.POST,request.FILES)
            if form.is_valid():
                form.save()
            else:
                form = ProductForm()
            # serializer = self.serializer_class(data=request.data)
            # if serializer.is_valid():
            #     serializer = serializer.save()
            #     status_code = status.HTTP_201_CREATED
            response = {'status' : 'success','status_code' : status.HTTP_201_CREATED,'message': 'Product created successfully'}
        except Exception as error:
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            response = {'status' : 'failure','status_code' : status.HTTP_500_INTERNAL_SERVER_ERROR,'message': str(error)}
        return Response(response)  

    def get(self,request):
        try:
            product_info = Products.objects.all()
            serializer = self.serializer_class(product_info,many=True)
            response = {'status' : 'success','status_code' : status.HTTP_200_OK,'message': 'Product retrived successfully',"list":serializer.data}
        except Exception as error:
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            response = {'status' : 'failure','status_code' : status.HTTP_500_INTERNAL_SERVER_ERROR,'message': str(error)}
        return Response(response) 

class ProductUpdateViewDeleyeById(UpdateAPIView,RetrieveAPIView,DestroyAPIView):
    serializer_class = ProductsSerializer
    permission_classes = (AllowAny,)
    userinfo = Products.objects.all()

    def get(self,request,id):
        try:
            product_info = Products.objects.get(product_id = id)
            serializer = self.serializer_class(product_info,many=False)
            response = {'status' : 'success','status_code' : status.HTTP_200_OK,'message': 'Product retrived successfully',"list":serializer.data}
        except Exception as error:
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            response = {'status' : 'failure','status_code' : status.HTTP_500_INTERNAL_SERVER_ERROR,'message': str(error)}
        return Response(response) 
    def put(self,request,id):
        try:
            product = Products.objects.get(product_id = id)
            if 'image_url' in request.FILES:
                image_url = request.FILES['image_url']
            form = ProductForm(request.data, request.FILES, instance=product)
            if form.is_valid():
                form.save()  
                response = {
                    'status': 'success',
                    'status_code': status.HTTP_200_OK,
                    'message': 'Product updated successfully'
                }
        except Exception as error:
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            response = {'status' : 'failure','status_code' : status.HTTP_500_INTERNAL_SERVER_ERROR,'message': str(error)}
        return Response(response)




class CategoryCreation(CreateAPIView):
    serializer_class = CategorySerializer
    permission_classes = (AllowAny,)
    userinfo = Category.objects.all()
    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                serializer = serializer.save()
                status_code = status.HTTP_201_CREATED
                response = {'status' : 'success','status_code' : status.HTTP_201_CREATED,'message': 'Categories created successfully'}
        except Exception as error:
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            response = {'status' : 'failure','status_code' : status.HTTP_500_INTERNAL_SERVER_ERROR,'message': str(error)}
        return Response(response)  
    def get(self,request):
        try:
            user_info = Category.objects.all()
            serializer = self.serializer_class(user_info,many=True)
            response = {"status":"success","message":"retrived successfully","details":serializer.data}

        except Exception as error:
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            response = {'status' : 'failure','status_code' : status.HTTP_500_INTERNAL_SERVER_ERROR,'message': str(error)}
        return Response(response)  


# views.py
# curl -X GET "http://127.0.0.1:8000/products/search/?category_name=electronics&min_price=100&max_price=500"



class ProductSearchView(RetrieveAPIView):
    permission_classes = (AllowAny,)
    def get(self, request):
        try:
            product_name = request.query_params.get('product_name', None)
            category_name = request.query_params.get('category_name', None)
            if category_name and product_name:
                products = Products.objects.filter(name__icontains = product_name)
                products = products.filter(category_id__name__icontains=category_name )
                category_ids = products.values_list('category_id', flat=True)
                print(category_ids,"????????????")
                parent_categories = Category.objects.filter(parent_category_id__in=category_ids)
                all_related_categories = list(set(category_ids) | set(parent_categories.values_list('category_id', flat=True)))
                products = Products.objects.filter(category_id__in=all_related_categories)

            min_price = request.query_params.get('min_price', None)
            max_price = request.query_params.get('max_price', None)
            if min_price:
                products = products.filter(price__gte=min_price)
            if max_price:
                products = products.filter(price__lte=max_price)

            serializer = ProductsSerializer(products, many=True)
            response = {
                'status': 'success',
                'status_code': status.HTTP_200_OK,
                'message': 'Products retrieved successfully',
                'products': serializer.data
            }
        except Exception as error:
            response = {
                'status': 'failure',
                'status_code': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'message': str(error)
            }

        return Response(response)

class AddToCart(CreateAPIView):
    serializer_class = CartSerializer
    permission_classes = (AllowAny,)
    def post(self,request):
        try:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                serializer = serializer.save()
                status_code = status.HTTP_201_CREATED
                response = {'status' : 'success','status_code' : status.HTTP_201_CREATED,'message': 'Cart created successfully'}
        except Exception as error:
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            response = {'status' : 'failure','status_code' : status.HTTP_500_INTERNAL_SERVER_ERROR,'message': str(error)}
        return Response(response) 


class AddToCartListDelete(RetrieveAPIView,DestroyAPIView):
    serializer_class = CartSerializer
    permission_classes = (AllowAny,)
    def get(self,request,id):
        try:
            print("55555555")
            cart = CartInfo.objects.filter(user_id = id)
            serializer = self.serializer_class(cart,many=True)
            response = {"status":"success","message":"retrived successfully","details":serializer.data}
        except Exception as error:
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            response = {'status' : 'failure','status_code' : status.HTTP_500_INTERNAL_SERVER_ERROR,'message': str(error)}
        return Response(response) 
    
    def delete(self,request,id):
        try:
            cart = CartInfo.objects.get(cart_id = id).delete()
            response = {"status":"success","message":"deleted successfully"}
        except Exception as error:
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            response = {'status' : 'failure','status_code' : status.HTTP_500_INTERNAL_SERVER_ERROR,'message': str(error)}
        return Response(response)      

class CreateOrderAndPayment(CreateAPIView):
    permission_classes = (AllowAny,)
    def post(self,request):
        try:
            order_items_data = request.data['order_items']
            total_amount = 0
            order_items = []
            for item in order_items_data:
                product = Products.objects.get(product_id=item['product_id'])
                quantity = item['quantity']
                price = product.price  
                total_amount += price * quantity 
                order_item = Order_items(
                    product_id=product,
                    quantity=quantity,
                    price=price,
                )
                order_items.append(order_item)
            user = Users.objects.get(user_id = request.data["user_id"])
            order = Orders_info.objects.create(user_id=user,total_amount=total_amount)
            for order_item in order_items:
                order_item.order_id = order
                order_item.save()
            payment = Payments.objects.create(order_id=order,payment_method='Stripe',transaction_id=random.randrange(1,500000,100000))
            time.sleep(5)
            payment = Payments.objects.get(payment_id = payment.payment_id)
            payment.payment_status = 'successful'
            payment.save()
            order = Orders_info.objects.get(order_id = order.order_id)
            order.order_status = 'paid'
            order.save()
            shipping = ShippingInfo.objects.create(order_id = order,tracking_number = random.randrange(1,990000000000000,10000000000000),shipping_address = request.data["shipping_address"])
            response = {"status":"success","message":"Created successfully"}
        except Exception as error:
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            response = {'status' : 'failure','status_code' : status.HTTP_500_INTERNAL_SERVER_ERROR,'message': str(error)}
        return Response(response)   
    
        