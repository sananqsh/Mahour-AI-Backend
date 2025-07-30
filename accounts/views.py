from rest_framework import status
from rest_framework.exceptions import ValidationError as DRFValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import CustomUser
from .serializers import UserRegistrationSerializer, PasswordChangeSerializer

class RegisterUserView(APIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_id="register_user",
        tags=["auth"],
        operation_description="Registers a new user. If successful, an OTP is generated.",
        request_body=UserRegistrationSerializer,
        responses={
            201: openapi.Response(
                description="User created successfully",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'message': openapi.Schema(type=openapi.TYPE_STRING, description='Success message'),
                    },
                ),
                examples={
                    "application/json": {
                        "message": "User created successfully"
                    }
                }
            ),
            400: openapi.Response(
                description="Bad request",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(type=openapi.TYPE_STRING, description='Error message'),
                    },
                ),
                examples={
                    "application/json": {
                        "detail": "Invalid email or password"
                    }
                }
            ),
        }
    )
    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                user = serializer.save()
                user.save()

                return Response({
                    "message": "User created successfully. Please verify your phone number with the OTP sent.",
                    "user_id": user.id
                }, status=status.HTTP_201_CREATED)
        except DRFValidationError as e:
            return Response({"detail": str(e.args[0])}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomTokenObtainPairView(TokenObtainPairView):
    @swagger_auto_schema(
        operation_id="obtain_token (login)",
        tags=["auth"],
        operation_description="Obtain JWT access and refresh tokens by providing valid credentials (login).",
        responses={
            200: openapi.Response(
                description="Tokens obtained successfully",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'access': openapi.Schema(type=openapi.TYPE_STRING, description='JWT access token'),
                        'refresh': openapi.Schema(type=openapi.TYPE_STRING, description='JWT refresh token'),
                    },
                ),
                examples={
                    "application/json": {
                        "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                        "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
                    }
                }
            ),
            400: openapi.Response(
                description="Bad request",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(type=openapi.TYPE_STRING, description='Error message'),
                    },
                ),
                examples={
                    "application/json": {
                        "detail": "No active account found with the given credentials."
                    }
                }
            ),
            401: openapi.Response(
                description="Unauthorized",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(type=openapi.TYPE_STRING, description='Error message'),
                    },
                ),
                examples={
                    "application/json": {
                        "detail": "Account is not active."
                    }
                }
            ),
            403: openapi.Response(
                description="Forbidden",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(type=openapi.TYPE_STRING, description='Error message'),
                    },
                ),
                examples={
                    "application/json": {
                        "detail": "Account needs OTP verification."
                    }
                }
            ),
        }
    )
    def post(self, request, *args, **kwargs):
        user = CustomUser.objects.filter(email=request.data.get('email')).first()
        if user:
            if not user.is_active:
                return Response({"detail": "Account is not active."}, status=status.HTTP_401_UNAUTHORIZED)

        return super().post(request, *args, **kwargs)

class CustomTokenRefreshView(TokenRefreshView):
    @swagger_auto_schema(
        operation_id="token_refresh",
        tags=["auth"],
        operation_description="Obtain a new access token by providing a valid refresh token.",
        responses={
            200: openapi.Response(
                description="New access token obtained successfully",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'access': openapi.Schema(type=openapi.TYPE_STRING, description='New JWT access token'),
                    },
                ),
                examples={
                    "application/json": {
                        "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
                    }
                }
            ),
            400: openapi.Response(
                description="Bad request",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(type=openapi.TYPE_STRING, description='Error message'),
                    },
                ),
                examples={
                    "application/json": {
                        "detail": "Token is invalid or expired."
                    }
                }
            ),
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

class PasswordChangeView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_id="change_password",
        tags=["auth"],
        operation_description="Changes the user's password. Requires authentication and current password.",
        request_body=PasswordChangeSerializer,
        responses={
            200: openapi.Response(
                description="Password changed successfully",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'message': openapi.Schema(type=openapi.TYPE_STRING, description='Success message'),
                    },
                ),
                examples={
                    "application/json": {
                        "message": "Password changed successfully."
                    }
                }
            ),
            400: openapi.Response(
                description="Bad request",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'error': openapi.Schema(type=openapi.TYPE_OBJECT, description='Error messages'),
                    },
                ),
                examples={
                    "application/json": {
                        "error": {
                            "current_password": "Current password is incorrect.",
                            "new_password": ["Password must be at least 8 characters long."]
                        }
                    }
                }
            ),
            401: "Authentication credentials were not provided.",
        }
    )
    def post(self, request):
        serializer = PasswordChangeSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            user = request.user
            # Set the new password
            user.set_password(serializer.validated_data['new_password'])
            user.save()

            # Invalidate all existing tokens to force logout on all devices
            RefreshToken.for_user(user)

            return Response({'message': 'Password changed successfully.'}, status=status.HTTP_200_OK)

        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
