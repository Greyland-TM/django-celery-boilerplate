from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from knox.models import AuthToken

from .serializers import UserSerializer, RegisterSerializer, LoginSerializer
from .models import Customer, Employee
# from apps.package_manager.utils import create_service_package
from datetime import datetime


class UserAPIView(generics.RetrieveAPIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class RegisterAPIView(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        # TODO - Add better validadtion and security
        print("\n\n**************\nSTARTING CUSTOMER SAVE\n")
        print(f"Registering user: {request.data['first_name']} {request.data['last_name']}")

        try:
            # This could use a cleaner solution...
            # If type and password are not sent in request then save as defaults here...
            try:
                request.data.update({"type": f"{request.data['type']}"})
            except:
                request.data.update({"type": "customer"})

            try:
                request.data.update({"password": f"{request.data['password']}"})
            except:
                request.data.update({"password": "app_2temppass2023"})

            try:
                request.data.update({"phone": f"{request.data['phone']}"})
            except:
                request.data.update({"phone": None})

            try:
                request.data.update({"username": f"{request.data['email']}"})
            except Exception as error:
                # TODO - Add better error handling
                print(f"\n  **************\n  Error: {error}")
                return Response({"ok": False}, status=status.HTTP_400_BAD_REQUEST)

            # Create base user. Checkout the serializer for more details
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()

            # If the Customer Registration was filled out create a new Customer
            if request.data["type"] == "customer":
                representative = Employee.objects.all().first() # TODO - Change this to the employee that is associated with the customer
                                   
                # Create the customer...
                customer = Customer(
                    user=user,
                    rep=representative,
                    first_name=request.data["first_name"],
                    last_name=request.data["last_name"],
                    email=request.data["email"],
                    phone=request.data["phone"],
                )

                if request.data["packages"]:
                    packages = request.data["packages"]
                    customer.save(packages_saved=packages)
                else:
                    customer.save()

            # If the Employee Registration was Filled out create a new Employee.
            if request.data["type"] == "employee":
                employee = Employee(
                    user=user,
                    first_name=request.data["first_name"],
                    last_name=request.data["last_name"],
                )
                employee.save()
                
            return Response(
                {
                    "ok": True,
                    "user": UserSerializer(
                        user, context=self.get_serializer_context()
                    ).data,
                    "token": AuthToken.objects.create(user)[1],
                },
                status=status.HTTP_200_OK,
            )
        except Exception as error:
            print(f"Error: {error}")
            return Response({"ok": False}, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data
            return Response(
                {
                    "user": UserSerializer(
                        user, context=self.get_serializer_context()
                    ).data,
                    "token": AuthToken.objects.create(user)[1],
                }
            )
        except Exception as error:
            print(f"Error: {error}")
            return Response({"ok": False}, status=status.HTTP_400_BAD_REQUEST)
