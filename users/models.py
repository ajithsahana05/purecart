from django.db import models
import uuid
from django.core.validators import RegexValidator
# from django.contrib.postgres.fields import ArrayField,JSONField
# Create your models here.
class Role(models.Model):
    role_name = models.CharField(max_length=100,null=False)
    class Meta:
        db_table = "Role_info"

class Users(models.Model):
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=100,null=False)
    last_name = models.CharField(max_length=100,null=False)
    email = models.EmailField(max_length = 254,unique=True,null=False)
    password = models.CharField(max_length=255,null=True)
    phone_number = models.CharField(max_length=15,validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$',message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")])
    address = models.CharField(max_length=500,null=False)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = "Users_info"

class Category(models.Model):
    category_id = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100,null=False)
    description = models.CharField(max_length=100,null=False)
    parent_category_id = models.ForeignKey("self", on_delete = models.CASCADE,null=True,blank=True)
    class Meta:
        db_table = "Categoty_info"

class Products(models.Model):
    product_id = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100,null=False)
    description = models.CharField(max_length=100,null=False)
    price = models.BigIntegerField()
    stock_quantity = models.BigIntegerField()
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE)
    image_url = models.FileField(upload_to='uploads/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = "Products_info"

class CartInfo(models.Model):
    cart_id = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False)
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.BigIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = "Cart_info"

class Orders_info(models.Model):
    order_id = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False)
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE)
    total_amount = models.BigIntegerField()
    order_status = models.CharField(max_length=100,default="pending")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = "Orders_info"

class Order_items(models.Model):
    order_item_id = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False)
    order_id = models.ForeignKey(Orders_info, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.BigIntegerField()
    price = models.BigIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = "Order_items"

class Payments(models.Model):
    payment_id = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False)
    order_id = models.ForeignKey(Orders_info, on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=100)
    payment_status = models.CharField(max_length=100,default="pending")
    transaction_id = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = "Payment_info"


class ShippingInfo(models.Model):
    shipping_id = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False)
    order_id = models.ForeignKey(Orders_info, on_delete=models.CASCADE)
    tracking_number = models.BigIntegerField()
    shipping_address = models.CharField(max_length=500,null=True)
    status = models.CharField(max_length=100,default='pending',null=True)
    estimated_delivery_date = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = "Shipping_info"

# class Inventory_info(models.Model):
#     inventory_id = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False)
#     product_id = models.ForeignKey(Orders_info, on_delete=models.CASCADE)
#     warehouse_location = models.CharField(max_length=255,null=True)
#     stock_level = models.BigIntegerField()
#     reorder_threshold = models.CharField(max_length=255,null=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     class Meta:
#         db_table = "Inventory_info"




# class ProductSearchView(APIView):
#     permission_classes = (AllowAny,)

#     def get(self, request):
#         try:
#             # Start by retrieving all products
#             products = Products.objects.all()

#             # Category filtering logic
#             category_name = request.query_params.get('category_name', None)
#             if category_name:
#                 products = products.filter(category_id__name__icontains=category_name)

#                 # Get categories and their parent categories
#                 category_ids = products.values_list('category_id', flat=True)
#                 parent_categories = Category.objects.filter(parent_category_id__in=category_ids)
#                 all_related_categories = list(set(category_ids) | set(parent_categories.values_list('category_id', flat=True)))

#                 # Apply filtering to include products from these categories
#                 products = products.filter(category_id__in=all_related_categories)

#             # Product name search logic
#             product_name = request.query_params.get('product_name', None)
#             if product_name:
#                 products = products.filter(name__icontains=product_name)

#             # Price filtering logic
#             min_price = request.query_params.get('min_price', None)
#             max_price = request.query_params.get('max_price', None)
#             if min_price:
#                 products = products.filter(price__gte=min_price)
#             if max_price:
#                 products = products.filter(price__lte=max_price)

#             # Serialize the products
#             serializer = ProductsSerializer(products, many=True)

#             # Prepare successful response
#             response = {
#                 'status': 'success',
#                 'status_code': status.HTTP_200_OK,
#                 'message': 'Products retrieved successfully',
#                 'products': serializer.data
#             }

#         except Exception as error:
#             # In case of any error, return failure response
#             response = {
#                 'status': 'failure',
#                 'status_code': status.HTTP_500_INTERNAL_SERVER_ERROR,
#                 'message': str(error)
#             }

#         return Response(response)
