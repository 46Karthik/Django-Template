from django.shortcuts import render  
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from master.views import  return_response,Decode_JWt
from rest_framework.pagination import PageNumberPagination
from django.db.models import Count, Q, Case, When, BooleanField, OuterRef, Subquery, DateField, F, Exists,IntegerField,Value,CharField,DateTimeField,ExpressionWrapper,Func,DurationField
class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'limit'
    max_page_size = 100


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
        refresh['role'] = user.profile.role.id
        refresh['role_name'] = user.profile.role.name
        return Response(return_response(2, 'Login successful', {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }), status=status.HTTP_201_CREATED)

class ProfileView(APIView):
    pagination_class = CustomPagination
    permission_classes = [IsAuthenticated]
    def get(self, request,id=None):
        if id is None:
            search = request.query_params.get('search')
            queryset = Profile.objects.all().order_by('-created_at')
            if search:
                queryset = queryset.filter(Q(name__icontains=search) | Q(email__icontains=search))
            paginator = self.pagination_class()
            paginated_queryset = paginator.paginate_queryset(queryset, request)
            serializer = ProfileSerializer(paginated_queryset, many=True)
            return paginator.get_paginated_response({
                "status": 2,
                "message": "Data found",
                "data": serializer.data or [],
                "count": paginator.page.paginator.count,
                "total_pages": paginator.page.paginator.num_pages
            })
        else:
            return Response(return_response(0, 'Invalid request'), status=status.HTTP_400_BAD_REQUEST)
    def put(self, request, id=None):
        print(request.headers.get('Authorization'))
        payload = Decode_JWt(request.headers.get('Authorization'))
        print(payload)
        if id is None:
            return Response(return_response(0, 'Invalid request'), status=status.HTTP_400_BAD_REQUEST)
        try:
            profile = Profile.objects.get(id=id)
        except Profile.DoesNotExist:
            return Response(return_response(0, 'Profile not found'), status=status.HTTP_400_BAD_REQUEST)
        if payload:
            request.data['updated_by'] = payload.get('name')
        user = profile.user
        serializer = RegisterSerializer(
            user,
            data=request.data,
            partial=True
        )   
        if serializer.is_valid():
            serializer.save()
            return Response(return_response(1, 'Success', serializer.data), status=status.HTTP_201_CREATED)
        return Response(return_response(0, 'Error', serializer.errors), status=status.HTTP_400_BAD_REQUEST)
