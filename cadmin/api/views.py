from rest_framework.generics import ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView,CreateAPIView, RetrieveUpdateAPIView
from rest_framework.views import APIView
from django.contrib.auth.models import User
from .serializers import UserCreateSerializer, UserLoginSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly
# from .permissions import IsOwnerOrReadOnly
from rest_framework.filters import SearchFilter
from rest_framework.response import Response


class UserCreateAPIView(CreateAPIView):
    serializer_class = UserCreateSerializer
    queryset = User.objects.all()

class UserLoginAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer
    queryset = User.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = UserLoginSerializer(data = request.data)
        if serializer.is_valid(raise_exception=True):
            new_data = serializer.data
            return Response(new_data)
        return Response(serializer.errors)
    
    