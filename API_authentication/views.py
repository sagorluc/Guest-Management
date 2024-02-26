from django.shortcuts import render
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from authentication.email_setup import send_otp_via_email
from API_authentication.models import User
# from django.contrib.auth.models import User
from API_authentication.renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import (
    AllowAny, IsAuthenticatedOrReadOnly, 
    IsAuthenticated, IsAdminUser
    )
from API_authentication.serializers import (
    UserRegistrationSerializer, 
    UserAccountVerificationSerializer,
    UserLoginSerializer, 
    UserSerializer,
    )
from API_authentication.validation import (
    custom_validation,
    validate_email,
    validate_password,
    validate_username
    )

# ======================== MAKE MANUAL TOKEN REFRESH AND ACCESS ==========================
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

# ========================== API USER REGISTRATION VIA EMAIL ============================
class UserRegistrationView(APIView):
    permission_classes = (AllowAny, )
    renderer_classes = [UserRenderer, ] # will show the visual error
     
    def post(self, request):
        try:
            clean_data = request.data
            serializer = UserRegistrationSerializer(data=clean_data)
            if serializer.is_valid(raise_exception=True):
                user = serializer.save()
                token = get_tokens_for_user(user)
                to_email = serializer.data['email']
                send_otp_via_email(to_email)
                context = {
                    'status': 200,
                    'token' : token,
                    'message': 'Registration successful. Check your email for verification.',
                    'data': serializer.data
                }
                return Response(context, status=status.HTTP_201_CREATED)
            
            context = {
                'status':  400,
                'message': 'Invalid data provided',
                'data': serializer.errors
            }
            return Response(context, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            print(e)
            context = {
                'status': 500,
                'message': 'Internal server error',
                'data': serializer.errors
            }
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# ============================ API VERIFICATION ACCOUNT VIA OTP ========================       
class UserVerifyAccountView(APIView):
    permission_classes = [AllowAny, ]
    renderer_classes = [UserRenderer, ]
    
    def post(self, request):
        try:
            data  = request.data
            serializer = UserAccountVerificationSerializer(data=data)
            if serializer.is_valid():
                email = serializer.data['email']
                otp = serializer.data['otp']
                
                user = User.objects.filter(email=email)
                
                if not user.exists():
                    contex = {
                        'status': 400,
                        'message': 'Wrong email. User email not found',
                        'data': serializer.errors
                    }
                    return Response(contex, status=status.HTTP_400_BAD_REQUEST)
                # print(user[0].verification_otp, '##############')
                if not user[0].verification_otp == otp:
                    contex = {
                        'status': 400,
                        'message': 'Wrong OTP. This OTP is not valid',
                        'data': serializer.errors
                    }
                    return Response(contex, status=status.HTTP_400_BAD_REQUEST)
                
                user = user.first()
                user.is_verified = True # without true user can not be login
                user.is_active = True   # without true user can not be login
                user.save()
                token = get_tokens_for_user(user)
                contex = {
                        'status': 200,
                        'token' : token,
                        'message': 'Account has been verified successfully',
                        'data': serializer.data
                    }
                return Response(contex, status=status.HTTP_200_OK)
                    
        except Exception as e:
            print(e)
            contex = {
                'status': 500,
                'message': 'Something went worng',
                'data': serializer.errors
            }
            return Response(contex, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                
                
            
# ================================= API ACCOUNT LOGIN ====================================
class UserLoginView(APIView):
    permission_classes = (AllowAny, )
    renderer_classes = [UserRenderer, ]
    authentication_classes = (SessionAuthentication, )
        
    def post(self, request):
        clean_data = request.data
        serializer = UserLoginSerializer(data=clean_data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            
            user = authenticate(email=email, password=password)
            
            if user:
                login(request, user)
                token = get_tokens_for_user(user)
                context = {
                    'status': 200,
                    'token' : token,
                    'message': 'Login successfully',
                    'data': serializer.data
                }
                return Response(context, status=status.HTTP_200_OK)
            else:
                context = {
                    'status': 400,
                    'errors': {'non_field_error': ['Email or password is not valid']},
                    'data': serializer.errors
                }
                return Response(context, status=status.HTTP_400_BAD_REQUEST)
        else:
            context = {
                'status': 500,
                'errors': 'Data is not valided',
                'data': serializer.errors
            }
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
# ================================= API ACCOUNT LOGOUT ===================================
class UserLogoutView(APIView):
    renderer_classes = [UserRenderer, ]
    def post(self, request):
        logout(request)
        context = {'message': 'Logout successfully!'}
        return Response(context, status=status.HTTP_200_OK)
    
    
# ==================================== API USER VIEW ====================================
class UserView(APIView):
    renderer_classes = [UserRenderer, ] 
    permission_classes = (IsAuthenticated, )
    authentication_classes = (SessionAuthentication, )
    
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response({'user': serializer.data}, status=status.HTTP_200_OK)
        
    
    