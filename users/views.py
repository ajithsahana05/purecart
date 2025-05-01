from django.shortcuts import render
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
import hashlib
# Create your views here.
class Test(RetrieveAPIView):
    serializer_class = UsersSerializer
    permission_classes = (AllowAny,)
    userinfo = Users.objects.all()
    def get(self,request):
        try:
            return Response({"status":"success","message":"Retrived successfully"},status=status.HTTP_200_OK) 
        except Exception as error:
            return Response({"status":"failure"},status=status.HTTP_400_BAD_REQUEST)






def hash_password(password):
    password_bytes = password.encode('utf-8')
    hash_object = hashlib.sha256(password_bytes)
    password_hash = hash_object.hexdigest()
    return password_hash

class UserRegistrationView(CreateAPIView): 
    serializer_class = UsersSerializer
    permission_classes = (AllowAny,)
    userinfo = Users.objects.all()
    def post(self, request):
        try:
            print(request.data)
            if 'email' in request.data:
                users = self.userinfo.filter(email = request.data["email"])
            if users.exists():
                status_code = status.HTTP_200_OK
                response = {'status' : 'failed','status_code' : status.HTTP_200_OK,'message': 'User already exist'}
            else:
                password = request.data["password"]
                hashed_password = hash_password(password)
                request.data["password"] = hashed_password
                serializer = self.serializer_class(data=request.data)
                if serializer.is_valid():
                    serializer=serializer.save()
                    status_code = status.HTTP_201_CREATED
                    response = {'status' : 'success','status_code' : status.HTTP_201_CREATED,'message': 'User registered successfully'}
        except Exception as error:
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            response = {'status' : 'failure','status_code' : status.HTTP_500_INTERNAL_SERVER_ERROR,'message': str(error)}
        return Response(response,status=status_code)
    

class UsersLogin(CreateAPIView):
    serializer_class = UsersSerializer
    permission_classes = (AllowAny,)
    userinfo = Users.objects.all()
    def post(self,request):
        try:
            email = self.userinfo.filter(email = request.data["email"])
            if not email.exists():
                status_code = status.HTTP_200_OK
                response = {'status':"failure","message":"Email not exists"}
            else:
                user_info = self.userinfo.get(email=request.data["email"])
                hashpassword = hash_password(request.data["password"])
                print(user_info.password,"????????",hashpassword)
                if user_info.password == hashpassword:
                    serializer = self.serializer_class(user_info,many=False)
                    status_code = status.HTTP_200_OK
                    response = {"status":"success","message":"User login successfully","user_details":serializer.data}
                else:
                    status_code = status.HTTP_200_OK
                    response = {'status':"failure","message":"Password mis-match"}
        except Exception as error:
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            response = {'status' : 'failure','status_code' : status.HTTP_500_INTERNAL_SERVER_ERROR,'message': str(error)}
        return Response(response,status=status_code)
    
class UsersUpdateListDelete(UpdateAPIView,RetrieveAPIView,DestroyAPIView):
    serializer_class = UsersSerializer
    permission_classes = (AllowAny,)
    user_info = Users.objects.all()
    def get(self,request,id):
        try:
            user_list = self.user_info.get(user_id=id)
            serilizer = self.serializer_class(user_list,many=False)
            response = {"status":"success","message":"retrived successfully","details":serilizer.data}
        except Exception as error:
            response = {"status":"failure","message":str(error)}
        return Response(response)
    def put(self,request,id):
        try:
            user = Users.objects.get(user_id = id)
            serializer = self.serializer_class(instance = user, data = request.data)
            # print(serializer)
            try:
                if serializer.is_valid():
                    print("000000")
                    serializer.save()
                    response = {"status":"success","message":"retrived successfully","details":serializer.data}
                else:
                    print(serializer.errors)
            except Exception as e:
                print(e)
        except Exception as error:
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            response = {'status' : 'failure','status_code' : status.HTTP_500_INTERNAL_SERVER_ERROR,'message': str(error)}
        return Response(response)
