from django.shortcuts import render  
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from master.views import  return_response


class RegisterView(APIView):
    def post(self, request):
        # check if email or username already exists
        if AuthUser.objects.filter(email=request.data['email']).exists():
            return Response(return_response(0, 'Email already exists'), status=status.HTTP_400_BAD_REQUEST)
        if AuthUser.objects.filter(username=request.data['username']).exists():
            return Response(return_response(0, 'Username already exists'), status=status.HTTP_400_BAD_REQUEST)
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(return_response(1, 'Success', serializer.data), status=status.HTTP_201_CREATED)
        return Response(return_response(0, 'Error', serializer.errors), status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']
        if not AuthUser.objects.filter(email=email).exists():
            return Response(return_response(0, 'Email not found'), status=status.HTTP_400_BAD_REQUEST)
        user = AuthUser.objects.get(email=email)
        if not user.check_password(password):
            return Response(return_response(0, 'Password not correct'), status=status.HTTP_400_BAD_REQUEST)
        # create token
        refresh = RefreshToken.for_user(user)
        refresh['email'] = user.email
        refresh['name'] = user.username
        return Response(return_response(2, 'Login successful', {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }), status=status.HTTP_201_CREATED)

class CRMView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request,id = None):
        if id is not None:
            crm = CRM.objects.get(crm_id=id)
            serializer = CRMSerializer(crm)
            return Response(return_response(2, 'Success', serializer.data), status=status.HTTP_200_OK)
        all_data = CRM.objects.all()
        serializer = CRMSerializer(all_data, many=True)
        return Response(return_response(2, 'Success', serializer.data), status=status.HTTP_200_OK)
    def post(self, request):
        serializer = CRMSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(return_response(2, 'Saved Successfully', serializer.data), status=status.HTTP_201_CREATED)
        return Response(return_response(0, 'Error', serializer.errors), status=status.HTTP_400_BAD_REQUEST)
    def put(self, request):
        crm_instance = CRM.objects.get(crm_id=request.data['crm_id'])
        serializer = CRMSerializer(crm_instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(return_response(2, 'Updated Successfully', serializer.data), status=status.HTTP_200_OK)
        return Response(return_response(0, 'Error', serializer.errors), status=status.HTTP_400_BAD_REQUEST)



class DashboardView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        all_data = CRM.objects.all()
        serializer = CRMSerializer(all_data, many=True)
        return Response(return_response(2, 'Success', serializer.data), status=status.HTTP_200_OK)
