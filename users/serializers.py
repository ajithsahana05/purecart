from rest_framework import serializers
from .models import *
from django import forms

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = "__all__"

class UsersSerializer(serializers.ModelSerializer):
    role_name = serializers.SerializerMethodField()
    class Meta:
        model = Users
        fields = "__all__"
        extra_kwargs = {'password': {'write_only': True}}
    def get_role_name(self,obj):
        return obj.role.role_name if obj.role else None
    
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"

class ProductsSerializer(serializers.ModelSerializer):
    category_name = serializers.SerializerMethodField()
    image_url = serializers.SerializerMethodField()
    class Meta:
        model = Products
        fields = "__all__"
    def get_category_name(self,obj):
        # print(obj.category_id.name,"?????????????")
        return obj.category_id.name if obj.category_id else None
    def get_image_url(self,obj):
        return f"E:/myenv/purecart_backend/media/{obj.image_url}" if obj.image_url else None

class ProductForm(forms.ModelForm):
    class Meta:
        model = Products
        # fields = ['name','description','price','stock_quantity','category_id','image_url']
        fields = "__all__"

class CartSerializer(serializers.ModelSerializer):
    product_details = serializers.SerializerMethodField()
    class Meta:
        model = CartInfo
        fields = "__all__"
    def get_product_details(self,obj):
        if obj.product_id:
            # product_info = Products.objects.get(product_id = obj.product_id.id)
            serializer = ProductsSerializer(obj.product_id,many=False)
            return serializer.data
        else:
            return None
        
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orders_info
        fields = "__all__"

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order_items
        fields = "__all__"

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payments
        fields = "__all__"