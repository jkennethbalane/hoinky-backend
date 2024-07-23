# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status, serializers
# from rest_framework.permissions import AllowAny
# from django.contrib.auth import authenticate
# from djoser.views import TokenCreateView
# from djoser.conf import settings
# from djoser.serializers import TokenCreateSerializer
# from rest_framework.authtoken.models import Token
# from .serializers.TokenSerializer import CustomTokenCreateSerializer

# class CustomTokenCreateView(TokenCreateView):
#     permission_classes = (AllowAny,)
#     serializer_class = CustomTokenCreateSerializer

#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.user
#         token, created = Token.objects.get_or_create(user=user)
#         return Response(
#             {
#                 'auth_token': token.key,
#                 'is_superuser': user.is_superuser
#             },
#             status=status.HTTP_200_OK
#         )
